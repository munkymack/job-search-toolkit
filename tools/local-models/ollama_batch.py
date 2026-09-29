#!/usr/bin/env python3
"""
ollama_batch.py — run one prompt over a folder of documents against a local Ollama box.

Exists because Open WebUI's WebSocket gives up long before a 4-core laptop CPU finishes
prefilling a few thousand tokens into a 30B MoE. This talks to /api/generate directly,
waits as long as it takes, chunks long inputs, and writes results to disk so a crash
halfway through a corpus does not cost you the whole run.

Stdlib only.

Usage:
    python3 ollama_batch.py --prompt prompts/storyblock-extract.md --input corpus/ --out out/blocks
    python3 ollama_batch.py -p prompts/voice-observe.md -i corpus/ -o out/voice --model gemma4:26b
    python3 ollama_batch.py -p prompts/x.md -i corpus/ -o out/x --chunk 1500 --dry-run

The prompt file is a template. `{document}` is replaced with the chunk text, and
`{filename}` with the source file name. If `{document}` is absent, the chunk is appended.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from voice_metrics import collect_files, load_document, split_paragraphs, words_of  # noqa: E402

DEFAULT_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
DEFAULT_MODEL = "qwen3:30b-a3b-instruct-2507-q4_K_M"


def chunk_document(text: str, target_words: int) -> list[str]:
    """
    Split on paragraph boundaries, packing up to target_words per chunk. A single paragraph
    longer than 1.25x the target gets hard-split on whitespace so one runaway block cannot
    overflow num_ctx and silently truncate.
    """
    hard_cap = int(target_words * 1.25)
    paras: list[str] = []
    for para in split_paragraphs(text):
        tokens = para.split()
        if len(tokens) > hard_cap:
            paras += [" ".join(tokens[i:i + target_words])
                      for i in range(0, len(tokens), target_words)]
        else:
            paras.append(para)

    chunks: list[str] = []
    buf: list[str] = []
    count = 0
    for para in paras:
        n = len(words_of(para))
        if buf and count + n > target_words:
            chunks.append("\n\n".join(buf))
            buf, count = [], 0
        buf.append(para)
        count += n
    if buf:
        chunks.append("\n\n".join(buf))
    return chunks or [text]


def generate(host: str, model: str, prompt: str, options: dict, timeout: int) -> tuple[str, dict]:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "keep_alive": -1,          # do not unload between calls, cold reloads are the whole problem
        "options": options,
    }
    req = urllib.request.Request(
        host.rstrip("/") + "/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    return body.get("response", ""), body


def rate(body: dict) -> str:
    ev, dur = body.get("eval_count"), body.get("eval_duration")
    pv, pdur = body.get("prompt_eval_count"), body.get("prompt_eval_duration")
    parts = []
    if ev and dur:
        parts.append(f"{ev / (dur / 1e9):.1f} t/s gen ({ev} tok)")
    if pv and pdur:
        parts.append(f"{pv / (pdur / 1e9):.1f} t/s prefill ({pv} tok)")
    if body.get("load_duration"):
        parts.append(f"load {body['load_duration'] / 1e9:.1f}s")
    return ", ".join(parts) or "no timing returned"


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", Path(name).stem.lower()).strip("-")


def warm(host: str, model: str, timeout: int) -> None:
    print(f"warming {model} ...", file=sys.stderr, flush=True)
    t0 = time.time()
    try:
        _, body = generate(host, model, "ok", {"num_predict": 1}, timeout)
    except urllib.error.URLError as e:
        print(f"cannot reach {host}: {e}", file=sys.stderr)
        raise SystemExit(2)
    print(f"warm in {time.time() - t0:.1f}s ({rate(body)})", file=sys.stderr, flush=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-p", "--prompt", type=Path, required=True, help="Prompt template file")
    ap.add_argument("-i", "--input", type=Path, required=True, help="Document or directory")
    ap.add_argument("-o", "--out", type=Path, required=True, help="Output directory")
    ap.add_argument("-m", "--model", default=DEFAULT_MODEL)
    ap.add_argument("--host", default=DEFAULT_HOST, help=f"default {DEFAULT_HOST}")
    ap.add_argument("--chunk", type=int, default=1500, help="Target words per chunk (default 1500)")
    ap.add_argument("--temperature", type=float, default=0.2)
    ap.add_argument("--num-ctx", type=int, default=8192)
    ap.add_argument("--num-predict", type=int, default=1200)
    ap.add_argument("--timeout", type=int, default=1800, help="Seconds per request (default 1800)")
    ap.add_argument("--force", action="store_true", help="Redo chunks that already have output")
    ap.add_argument("--dry-run", action="store_true", help="Show the plan, call nothing")
    args = ap.parse_args()

    template = args.prompt.read_text(encoding="utf-8")
    files = collect_files(args.input)
    if not files:
        print(f"no readable files in {args.input}", file=sys.stderr)
        return 1

    jobs: list[tuple[Path, int, int, str]] = []
    for path in files:
        chunks = chunk_document(load_document(path), args.chunk)
        for idx, chunk in enumerate(chunks, 1):
            jobs.append((path, idx, len(chunks), chunk))

    total_words = sum(len(words_of(c)) for _, _, _, c in jobs)
    print(f"{len(files)} files -> {len(jobs)} chunks, ~{total_words:,} words "
          f"({args.chunk} words/chunk)", file=sys.stderr)

    if args.dry_run:
        for path, idx, n, chunk in jobs:
            print(f"  {path.name} [{idx}/{n}] {len(words_of(chunk)):>5} words")
        return 0

    args.out.mkdir(parents=True, exist_ok=True)
    options = {
        "temperature": args.temperature,
        "num_ctx": args.num_ctx,
        "num_predict": args.num_predict,
    }

    warm(args.host, args.model, args.timeout)

    started = time.time()
    done = failed = skipped = 0
    for i, (path, idx, n, chunk) in enumerate(jobs, 1):
        stem = f"{slug(path.name)}--{idx:02d}of{n:02d}"
        dest = args.out / f"{stem}.md"
        if dest.exists() and not args.force:
            skipped += 1
            continue

        prompt = template
        prompt = prompt.replace("{filename}", path.name)
        prompt = prompt.replace("{document}", chunk) if "{document}" in prompt \
            else prompt + "\n\n---\n\n" + chunk

        label = f"[{i}/{len(jobs)}] {path.name} {idx}/{n}"
        print(f"{label} ...", file=sys.stderr, flush=True)
        t0 = time.time()
        try:
            text, body = generate(args.host, args.model, prompt, options, args.timeout)
        except Exception as e:  # noqa: BLE001 - one bad chunk should not kill the run
            failed += 1
            print(f"{label} FAILED after {time.time() - t0:.0f}s: {e}", file=sys.stderr)
            (args.out / f"{stem}.error.txt").write_text(str(e), encoding="utf-8")
            continue

        header = (f"<!-- source: {path} | chunk {idx}/{n} | model: {args.model} | "
                  f"{rate(body)} -->\n\n")
        dest.write_text(header + text.strip() + "\n", encoding="utf-8")
        done += 1
        print(f"{label} {time.time() - t0:.0f}s, {rate(body)}", file=sys.stderr, flush=True)

    mins = (time.time() - started) / 60
    print(f"\ndone: {done} written, {skipped} already present, {failed} failed, "
          f"{mins:.1f} min total -> {args.out}", file=sys.stderr)
    return 1 if failed and not done else 0


if __name__ == "__main__":
    raise SystemExit(main())
