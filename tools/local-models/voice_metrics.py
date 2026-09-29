#!/usr/bin/env python3
"""
voice_metrics.py — mechanical measurement of a writing corpus.

This does the half of voice analysis that a language model does badly: exact,
countable facts about rhythm, punctuation, vocabulary, and habitual constructions.
It makes no qualitative judgments. The output is meant to be handed to a human or
a large hosted model as evidence, not read as a conclusion.

Stdlib only. No pip install, no network, runs anywhere Python 3.9+ runs.

Usage:
    python3 voice_metrics.py corpus/
    python3 voice_metrics.py corpus/ --per-file
    python3 voice_metrics.py corpus/ --baseline reference/ -o out/voice-metrics.md
    python3 voice_metrics.py corpus/ --json out/voice-metrics.json

Supported inputs: .md .markdown .txt .docx
"""

from __future__ import annotations

import argparse
import html
import json
import math
import re
import statistics
import sys
import zipfile
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

SUPPORTED = {".md", ".markdown", ".txt", ".text", ".docx"}

# ---------------------------------------------------------------------------
# Word lists
# ---------------------------------------------------------------------------

STOPWORDS = {
    "a", "about", "after", "all", "also", "am", "an", "and", "any", "are", "as",
    "at", "back", "be", "because", "been", "before", "being", "but", "by", "can",
    "could", "did", "do", "does", "doing", "done", "down", "each", "even", "for",
    "from", "get", "got", "had", "has", "have", "having", "he", "her", "here",
    "hers", "him", "his", "how", "i", "if", "in", "into", "is", "it", "its",
    "just", "like", "make", "makes", "many", "me", "might", "more", "most",
    "much", "must", "my", "no", "not", "now", "of", "off", "on", "one", "only",
    "or", "other", "our", "out", "over", "own", "ral", "said", "same", "say",
    "see", "she", "should", "so", "some", "such", "than", "that", "the", "their",
    "them", "then", "there", "these", "they", "this", "those", "through", "to",
    "too", "up", "us", "very", "was", "we", "well", "were", "what", "when",
    "where", "which", "while", "who", "why", "will", "with", "would", "you",
    "your", "yours",
}

# Terms named in CLAUDE.md as AI tells or banned, plus the usual suspects.
AI_TELLS = [
    "leverage", "leveraging", "leveraged", "leverages",
    "utilize", "utilizing", "utilized", "utilizes",
    "synergy", "synergies", "synergistic",
    "unlock", "unlocking", "unlocks",
    "seamless", "seamlessly",
    "robust", "powerful", "innovative", "cutting-edge", "best-in-class",
    "passionate", "passion", "results-driven", "dynamic",
    "elevate", "elevating", "empower", "empowering",
    "navigate", "navigating", "landscape", "realm", "tapestry",
    "delve", "delving", "underscore", "underscores",
    "holistic", "bespoke", "curated", "transformative", "game-changing",
    "streamline", "streamlined", "optimize", "optimized",
    "ecosystem", "paradigm", "actionable", "impactful",
]

HEDGES = [
    "arguably", "somewhat", "fairly", "rather", "quite", "perhaps", "maybe",
    "possibly", "generally", "typically", "essentially", "basically",
    "relatively", "sort of", "kind of", "a bit", "tends to", "may well",
]

INTENSIFIERS = [
    "very", "really", "extremely", "incredibly", "truly", "absolutely",
    "completely", "totally", "highly", "deeply", "hugely", "massively",
]

CONJUNCTION_OPENERS = {"but", "and", "so", "or", "yet", "because", "still", "then"}

IRREGULAR_PARTICIPLES = {
    "done", "made", "given", "taken", "seen", "known", "shown", "written",
    "built", "sent", "held", "found", "kept", "left", "told", "brought",
    "bought", "caught", "chosen", "driven", "run", "won", "lost", "put",
    "set", "cut", "read", "led", "met", "paid", "sold", "spent",
}

ABBREVIATIONS = {
    "mr", "mrs", "ms", "dr", "prof", "sr", "jr", "st", "vs", "etc", "inc",
    "ltd", "co", "corp", "dept", "est", "fig", "approx", "vol", "no", "jan",
    "feb", "mar", "apr", "jun", "jul", "aug", "sep", "sept", "oct", "nov", "dec",
    "e.g", "i.e", "u.s", "u.k", "a.m", "p.m",
}

# ---------------------------------------------------------------------------
# Loading and cleaning
# ---------------------------------------------------------------------------


def read_docx(path: Path) -> str:
    """Pull visible text out of a .docx without python-docx."""
    with zipfile.ZipFile(path) as z:
        try:
            xml = z.read("word/document.xml").decode("utf-8", "replace")
        except KeyError:
            return ""
    xml = re.sub(r"<w:p\b[^>]*/>", "\n\n", xml)
    xml = re.sub(r"</w:p>", "\n\n", xml)
    xml = re.sub(r"<w:br\b[^>]*/>", "\n", xml)
    xml = re.sub(r"<w:tab\b[^>]*/>", " ", xml)
    text = re.sub(r"<[^>]+>", "", xml)
    return html.unescape(text)


def strip_markdown(text: str) -> str:
    """Remove markup so we measure prose, not syntax."""
    # YAML frontmatter
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.DOTALL)
    # fenced code
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"~~~.*?~~~", "", text, flags=re.DOTALL)
    # inline code
    text = re.sub(r"`[^`\n]+`", "", text)
    # images then links, keeping link text
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    # html tags
    text = re.sub(r"<[^>]+>", "", text)
    # heading markers, blockquotes, list bullets, table pipes
    text = re.sub(r"^\s{0,3}#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s{0,3}>\s?", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s{0,3}([-*+]|\d+\.)\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\|.*\|\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*[-*_]{3,}\s*$", "", text, flags=re.MULTILINE)
    # emphasis markers
    text = re.sub(r"(\*\*|__|\*|_)", "", text)
    return text


def load_document(path: Path) -> str:
    if path.suffix.lower() == ".docx":
        raw = read_docx(path)
    else:
        raw = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() in {".md", ".markdown"}:
        raw = strip_markdown(raw)
    # normalize quotes and spaces, but leave dashes alone (we count them)
    raw = raw.replace("’", "'").replace("‘", "'")
    raw = raw.replace("“", '"').replace("”", '"')
    raw = raw.replace(" ", " ")
    return raw


def collect_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    files = sorted(p for p in root.rglob("*") if p.suffix.lower() in SUPPORTED and p.is_file())
    return [p for p in files if not p.name.startswith(".")]


# ---------------------------------------------------------------------------
# Segmentation
# ---------------------------------------------------------------------------

_SENT_SPLIT = re.compile(r'(?<=[.!?])["\')\]]*\s+')
_WORD = re.compile(r"[A-Za-z][A-Za-z'\-]*")


def split_paragraphs(text: str) -> list[str]:
    parts = re.split(r"\n\s*\n+", text)
    return [re.sub(r"\s+", " ", p).strip() for p in parts if p.strip()]


def split_sentences(paragraph: str) -> list[str]:
    pieces = _SENT_SPLIT.split(paragraph)
    merged: list[str] = []
    for piece in pieces:
        piece = piece.strip()
        if not piece:
            continue
        if merged:
            tail = merged[-1].rstrip()
            last = re.split(r"[\s]", tail)[-1].rstrip(".").lower()
            # rejoin false breaks: abbreviations, initials, decimals
            if last in ABBREVIATIONS or re.fullmatch(r"[a-z]", last) or re.search(r"\d$", tail):
                merged[-1] = tail + " " + piece
                continue
        merged.append(piece)
    return merged


def words_of(text: str) -> list[str]:
    return _WORD.findall(text)


def count_syllables(word: str) -> int:
    w = word.lower().strip("'-")
    if not w:
        return 0
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    return max(1, len(re.findall(r"[aeiouy]{1,2}", w)))


# ---------------------------------------------------------------------------
# Measurement
# ---------------------------------------------------------------------------


@dataclass
class DocStats:
    name: str
    paragraphs: int = 0
    sentences: int = 0
    words: int = 0
    sent_lengths: list[int] = field(default_factory=list)
    para_sent_counts: list[int] = field(default_factory=list)
    para_word_counts: list[int] = field(default_factory=list)
    syllables: int = 0
    word_counts: Counter = field(default_factory=Counter)
    openers: Counter = field(default_factory=Counter)
    punctuation: Counter = field(default_factory=Counter)
    phrases: Counter = field(default_factory=Counter)
    ai_tells: Counter = field(default_factory=Counter)
    hedges: Counter = field(default_factory=Counter)
    intensifiers: Counter = field(default_factory=Counter)
    contractions: int = 0
    passive_hits: int = 0
    questions: int = 0
    tricolons: int = 0
    conj_openers: int = 0
    first_person_sing: int = 0
    first_person_plur: int = 0
    second_person: int = 0
    numerals: int = 0
    type_tokens: list[str] = field(default_factory=list)


def measure(name: str, text: str) -> DocStats:
    s = DocStats(name=name)

    s.punctuation["em dash"] = text.count("—") + len(re.findall(r"(?<!-)--(?!-)", text))
    s.punctuation["en dash"] = text.count("–")
    s.punctuation["semicolon"] = text.count(";")
    s.punctuation["colon"] = text.count(":")
    s.punctuation["comma"] = text.count(",")
    s.punctuation["parenthetical"] = text.count("(")
    s.punctuation["exclamation"] = text.count("!")
    s.punctuation["ellipsis"] = text.count("…") + len(re.findall(r"\.\.\.", text))

    lowered = text.lower()
    for term in AI_TELLS:
        n = len(re.findall(r"\b" + re.escape(term) + r"\b", lowered))
        if n:
            s.ai_tells[term] += n
    for term in HEDGES:
        n = len(re.findall(r"\b" + re.escape(term) + r"\b", lowered))
        if n:
            s.hedges[term] += n
    for term in INTENSIFIERS:
        n = len(re.findall(r"\b" + re.escape(term) + r"\b", lowered))
        if n:
            s.intensifiers[term] += n

    s.contractions = len(re.findall(r"\b\w+'(?:t|re|ve|ll|d|m)\b", lowered))
    s.tricolons = len(re.findall(r"\b\w+,\s+\w+,?\s+and\s+\w+\b", lowered))
    s.numerals = len(re.findall(r"\b\d[\d,.]*%?\b", text))

    for para in split_paragraphs(text):
        sentences = split_sentences(para)
        if not sentences:
            continue
        s.paragraphs += 1
        s.para_sent_counts.append(len(sentences))
        s.para_word_counts.append(len(words_of(para)))

        for sent in sentences:
            w = words_of(sent)
            if not w:
                continue
            s.sentences += 1
            s.words += len(w)
            s.sent_lengths.append(len(w))
            s.syllables += sum(count_syllables(x) for x in w)
            if sent.rstrip().endswith("?"):
                s.questions += 1

            first = w[0].lower()
            s.openers[first] += 1
            if first in CONJUNCTION_OPENERS:
                s.conj_openers += 1

            low = [x.lower() for x in w]
            s.type_tokens.extend(low)
            s.word_counts.update(low)
            s.first_person_sing += sum(1 for x in low if x in {"i", "me", "my", "mine"})
            s.first_person_plur += sum(1 for x in low if x in {"we", "us", "our", "ours"})
            s.second_person += sum(1 for x in low if x in {"you", "your", "yours"})

            for i in range(len(low) - 1):
                if low[i] in {"was", "were", "is", "are", "been", "being", "be"}:
                    nxt = low[i + 1]
                    if nxt.endswith("ed") or nxt in IRREGULAR_PARTICIPLES:
                        s.passive_hits += 1

            content = [x for x in low if x not in STOPWORDS and len(x) > 2]
            for i in range(len(content) - 1):
                s.phrases[content[i] + " " + content[i + 1]] += 1
            for i in range(len(content) - 2):
                s.phrases[" ".join(content[i:i + 3])] += 1

    return s


def merge(stats: list[DocStats], name: str = "CORPUS") -> DocStats:
    total = DocStats(name=name)
    for s in stats:
        total.paragraphs += s.paragraphs
        total.sentences += s.sentences
        total.words += s.words
        total.syllables += s.syllables
        total.sent_lengths += s.sent_lengths
        total.para_sent_counts += s.para_sent_counts
        total.para_word_counts += s.para_word_counts
        total.word_counts += s.word_counts
        total.openers += s.openers
        total.punctuation += s.punctuation
        total.phrases += s.phrases
        total.ai_tells += s.ai_tells
        total.hedges += s.hedges
        total.intensifiers += s.intensifiers
        total.contractions += s.contractions
        total.passive_hits += s.passive_hits
        total.questions += s.questions
        total.tricolons += s.tricolons
        total.conj_openers += s.conj_openers
        total.first_person_sing += s.first_person_sing
        total.first_person_plur += s.first_person_plur
        total.second_person += s.second_person
        total.numerals += s.numerals
        total.type_tokens += s.type_tokens
    return total


# ---------------------------------------------------------------------------
# Derived numbers
# ---------------------------------------------------------------------------


def mattr(tokens: list[str], window: int = 100) -> float:
    """Moving-average type-token ratio. Length-independent, unlike plain TTR."""
    if len(tokens) < window:
        return len(set(tokens)) / len(tokens) if tokens else 0.0
    ratios = []
    counts: Counter = Counter(tokens[:window])
    ratios.append(len(counts) / window)
    for i in range(window, len(tokens)):
        out, inn = tokens[i - window], tokens[i]
        counts[out] -= 1
        if counts[out] == 0:
            del counts[out]
        counts[inn] += 1
        ratios.append(len(counts) / window)
    return sum(ratios) / len(ratios)


def flesch_reading_ease(words: int, sentences: int, syllables: int) -> float:
    if not words or not sentences:
        return 0.0
    return 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)


def flesch_kincaid_grade(words: int, sentences: int, syllables: int) -> float:
    if not words or not sentences:
        return 0.0
    return 0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59


def log_odds(corpus: Counter, baseline: Counter, alpha: float = 500.0):
    """
    Log-odds ratio with an informative Dirichlet prior (Monroe, Colaresi & Quinn).
    Returns [(word, z, corpus_rate_per_1k, baseline_rate_per_1k)] sorted by z.
    Positive z means you use it more than the baseline does.
    """
    n_c = sum(corpus.values())
    n_b = sum(baseline.values())
    if not n_c or not n_b:
        return []
    combined = corpus + baseline
    n_all = n_c + n_b
    out = []
    for word, y_c in corpus.items():
        y_b = baseline.get(word, 0)
        if y_c + y_b < 5:
            continue
        a_i = alpha * combined[word] / n_all
        num_c = y_c + a_i
        den_c = n_c + alpha - num_c
        num_b = y_b + a_i
        den_b = n_b + alpha - num_b
        if den_c <= 0 or den_b <= 0:
            continue
        delta = math.log(num_c / den_c) - math.log(num_b / den_b)
        var = 1.0 / num_c + 1.0 / num_b
        out.append((word, delta / math.sqrt(var), 1000 * y_c / n_c, 1000 * y_b / n_b))
    out.sort(key=lambda r: r[1], reverse=True)
    return out


def bucket(lengths: list[int]) -> list[tuple[str, int, float]]:
    edges = [(0, 5), (6, 10), (11, 15), (16, 20), (21, 25), (26, 30), (31, 40), (41, 10_000)]
    labels = ["1-5", "6-10", "11-15", "16-20", "21-25", "26-30", "31-40", "41+"]
    total = len(lengths) or 1
    rows = []
    for (lo, hi), label in zip(edges, labels):
        n = sum(1 for x in lengths if lo <= x <= hi)
        rows.append((label, n, 100 * n / total))
    return rows


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def per_k(n: int, words: int) -> float:
    return 1000 * n / words if words else 0.0


def sparkbar(pct: float, width: int = 24) -> str:
    filled = int(round(pct / 100 * width))
    return "█" * filled + "·" * (width - filled)


def build_report(total: DocStats, per_doc: list[DocStats], baseline: Counter | None,
                 show_per_file: bool) -> str:
    L = total.sent_lengths
    w = total.words
    out: list[str] = []
    a = out.append

    a("# Voice metrics")
    a("")
    a("Mechanical measurements only. Nothing here is a judgment about whether the writing")
    a("is good. Numbers are evidence for a human or a large model to interpret.")
    a("")
    a(f"**Corpus:** {len(per_doc)} document{'' if len(per_doc) == 1 else 's'}, {total.words:,} words, "
      f"{total.sentences:,} sentences, {total.paragraphs:,} paragraphs")
    a("")

    # -- rhythm
    a("## Rhythm")
    a("")
    if L:
        mean = statistics.mean(L)
        sd = statistics.pstdev(L) if len(L) > 1 else 0.0
        a(f"- Mean sentence length: **{mean:.1f} words**")
        a(f"- Median: {statistics.median(L):.0f} words")
        a(f"- Standard deviation: {sd:.1f}")
        a(f"- Burstiness (sd / mean): **{sd / mean:.2f}** "
          f"(under 0.45 reads metronomic, over 0.65 reads varied)")
        a(f"- Shortest: {min(L)} {'word' if min(L) == 1 else 'words'}. Longest: {max(L)} words.")
        a(f"- Very short sentences (5 words or fewer): {sum(1 for x in L if x <= 5)} "
          f"({100 * sum(1 for x in L if x <= 5) / len(L):.1f}%)")
        a(f"- Long sentences (over 30 words): {sum(1 for x in L if x > 30)} "
          f"({100 * sum(1 for x in L if x > 30) / len(L):.1f}%)")
        a("")
        a("Sentence length distribution:")
        a("")
        a("```")
        for label, n, pct in bucket(L):
            a(f"{label:>5} words  {sparkbar(pct)}  {pct:5.1f}%  ({n})")
        a("```")
    a("")
    if total.para_sent_counts:
        a(f"- Mean paragraph: {statistics.mean(total.para_sent_counts):.1f} sentences, "
          f"{statistics.mean(total.para_word_counts):.0f} words")
        a(f"- One-sentence paragraphs: "
          f"{sum(1 for x in total.para_sent_counts if x == 1)} "
          f"({100 * sum(1 for x in total.para_sent_counts if x == 1) / len(total.para_sent_counts):.1f}%)")
    a("")

    # -- readability
    a("## Readability")
    a("")
    a(f"- Flesch reading ease: **{flesch_reading_ease(w, total.sentences, total.syllables):.1f}** "
      f"(60-70 is plain English, under 50 is dense)")
    a(f"- Flesch-Kincaid grade: {flesch_kincaid_grade(w, total.sentences, total.syllables):.1f}")
    a(f"- Mean syllables per word: {total.syllables / w:.2f}" if w else "")
    a(f"- Vocabulary richness (MATTR-100): {mattr(total.type_tokens):.3f}")
    a("")

    # -- punctuation
    a("## Punctuation habits")
    a("")
    a("Rate is per 1,000 words.")
    a("")
    a("| Mark | Count | Per 1k words |")
    a("|---|---:|---:|")
    for mark, n in sorted(total.punctuation.items(), key=lambda kv: -kv[1]):
        a(f"| {mark} | {n} | {per_k(n, w):.1f} |")
    a("")
    a(f"- Questions: {total.questions} ({100 * total.questions / total.sentences:.1f}% of sentences)"
      if total.sentences else "")
    a(f"- Contractions: {total.contractions} ({per_k(total.contractions, w):.1f} per 1k words). "
      f"Possessive apostrophes are excluded, but this is still a rough count.")
    a("")

    # -- construction
    a("## Habitual constructions")
    a("")
    a("| Pattern | Count | Per 1k words |")
    a("|---|---:|---:|")
    a(f"| Sentences opening with a conjunction | {total.conj_openers} | "
      f"{per_k(total.conj_openers, w):.1f} |")
    a(f"| Tricolons (`x, y, and z`) | {total.tricolons} | {per_k(total.tricolons, w):.1f} |")
    a(f"| Probable passive voice | {total.passive_hits} | {per_k(total.passive_hits, w):.1f} |")
    a(f"| First person singular (I, me, my) | {total.first_person_sing} | "
      f"{per_k(total.first_person_sing, w):.1f} |")
    a(f"| First person plural (we, us, our) | {total.first_person_plur} | "
      f"{per_k(total.first_person_plur, w):.1f} |")
    a(f"| Second person (you, your) | {total.second_person} | "
      f"{per_k(total.second_person, w):.1f} |")
    a(f"| Numerals and percentages | {total.numerals} | {per_k(total.numerals, w):.1f} |")
    a("")
    a("Passive voice detection is a heuristic (`be` + participle) with no part-of-speech")
    a("tagging behind it. Treat the number as directional and spot-check before quoting it.")
    a("")

    # -- openers
    a("## Sentence openers")
    a("")
    a("The words you reach for to start a sentence. Heavy concentration at the top means a tic.")
    a("")
    a("| Opener | Count | % of sentences |")
    a("|---|---:|---:|")
    for word, n in total.openers.most_common(20):
        a(f"| {word} | {n} | {100 * n / total.sentences:.1f}% |" if total.sentences else "")
    a("")

    # -- vocabulary
    a("## Vocabulary")
    a("")
    if baseline:
        rows = log_odds(total.word_counts, baseline)
        func = [r for r in rows if r[0] in STOPWORDS]
        content_rows = [r for r in rows if r[0] not in STOPWORDS]
        a("Ranked by log-odds z-score with an informative Dirichlet prior. A z over 2 is a real")
        a("difference, not sampling noise. Positive means you use it more than the baseline does.")
        a("")
        a("### Function words")
        a("")
        a("The load-bearing table for voice. Function-word rates are what authorship attribution")
        a("actually runs on, because they are close to unconscious and survive across subjects.")
        a("")
        a("| Word | z | Yours /1k | Baseline /1k |")
        a("|---|---:|---:|---:|")
        for word, z, rc, rb in func[:15]:
            a(f"| {word} | {z:+.1f} | {rc:.2f} | {rb:.2f} |")
        for word, z, rc, rb in func[-10:][::-1]:
            a(f"| {word} | {z:+.1f} | {rc:.2f} | {rb:.2f} |")
        a("")
        a("### Content words")
        a("")
        a("Mostly subject matter rather than voice, unless the same word keeps showing up across")
        a("unrelated topics. Then it is a habit.")
        a("")
        a("| Word | z | Yours /1k | Baseline /1k |")
        a("|---|---:|---:|---:|")
        for word, z, rc, rb in content_rows[:25]:
            a(f"| {word} | {z:+.1f} | {rc:.2f} | {rb:.2f} |")
    else:
        a("No baseline supplied, so this is raw frequency with function words removed.")
        a("Run again with `--baseline DIR` pointed at reference writing (generic marketing copy,")
        a("or AI-generated drafts) to see what is actually distinctive rather than merely common.")
        a("")
        a("| Word | Count | Per 1k words |")
        a("|---|---:|---:|")
        content = Counter({k: v for k, v in total.word_counts.items()
                           if k not in STOPWORDS and len(k) > 2})
        for word, n in content.most_common(35):
            a(f"| {word} | {n} | {per_k(n, w):.2f} |")
    a("")

    # -- phrases
    a("## Repeated phrases")
    a("")
    a("Content-word bigrams and trigrams appearing three or more times. Signature phrasing,")
    a("or a crutch. The metrics cannot tell you which.")
    a("")
    repeated = [(p, n) for p, n in total.phrases.most_common(40) if n >= 3]
    if repeated:
        a("| Phrase | Count |")
        a("|---|---:|")
        for phrase, n in repeated[:30]:
            a(f"| {phrase} | {n} |")
    else:
        a("_None found at that threshold._")
    a("")

    # -- tells
    a("## AI tells and filler")
    a("")
    a("Terms flagged in the project's writing rules. Presence in your own past work is worth")
    a("knowing: it tells you whether a rule is describing you or correcting you.")
    a("")
    if total.ai_tells:
        a("| Term | Count | Per 1k words |")
        a("|---|---:|---:|")
        for term, n in total.ai_tells.most_common():
            a(f"| {term} | {n} | {per_k(n, w):.2f} |")
    else:
        a("_No flagged terms found._")
    a("")
    a(f"- Hedges: {sum(total.hedges.values())} total "
      f"({per_k(sum(total.hedges.values()), w):.1f} per 1k). "
      f"Top: {', '.join(f'{k} ({v})' for k, v in total.hedges.most_common(5)) or 'none'}")
    a(f"- Intensifiers: {sum(total.intensifiers.values())} total "
      f"({per_k(sum(total.intensifiers.values()), w):.1f} per 1k). "
      f"Top: {', '.join(f'{k} ({v})' for k, v in total.intensifiers.most_common(5)) or 'none'}")
    a("")

    # -- per file
    if show_per_file and len(per_doc) > 1:
        a("## Per document")
        a("")
        a("Variance across pieces is the interesting column. A voice that holds steady across")
        a("agency and in-house work is a different finding from one that shifts by context.")
        a("")
        a("| Document | Words | Mean sent | Burstiness | Flesch | Contractions /1k | Tells |")
        a("|---|---:|---:|---:|---:|---:|---:|")
        for d in sorted(per_doc, key=lambda x: -x.words):
            if not d.sent_lengths:
                continue
            m = statistics.mean(d.sent_lengths)
            sd = statistics.pstdev(d.sent_lengths) if len(d.sent_lengths) > 1 else 0.0
            a(f"| {d.name} | {d.words:,} | {m:.1f} | {sd / m:.2f} | "
              f"{flesch_reading_ease(d.words, d.sentences, d.syllables):.0f} | "
              f"{per_k(d.contractions, d.words):.1f} | {sum(d.ai_tells.values())} |")
        a("")

    a("---")
    a("")
    a("Generated by `voice_metrics.py`. Counts are exact; the labels attached to them are not")
    a("conclusions. Hand this to a model alongside three or four full samples and ask what")
    a("the numbers imply, rather than asking it to describe the voice cold.")
    a("")
    return "\n".join(x for x in out if x is not None)


def to_dict(total: DocStats, per_doc: list[DocStats]) -> dict:
    L = total.sent_lengths
    mean = statistics.mean(L) if L else 0.0
    sd = statistics.pstdev(L) if len(L) > 1 else 0.0
    return {
        "documents": len(per_doc),
        "words": total.words,
        "sentences": total.sentences,
        "paragraphs": total.paragraphs,
        "sentence_length": {
            "mean": round(mean, 2),
            "median": statistics.median(L) if L else 0,
            "stdev": round(sd, 2),
            "burstiness": round(sd / mean, 3) if mean else 0.0,
            "min": min(L) if L else 0,
            "max": max(L) if L else 0,
            "distribution": {label: n for label, n, _ in bucket(L)},
        },
        "readability": {
            "flesch_reading_ease": round(
                flesch_reading_ease(total.words, total.sentences, total.syllables), 2),
            "flesch_kincaid_grade": round(
                flesch_kincaid_grade(total.words, total.sentences, total.syllables), 2),
            "mattr_100": round(mattr(total.type_tokens), 4),
        },
        "punctuation_per_1k": {k: round(per_k(v, total.words), 3)
                               for k, v in total.punctuation.items()},
        "constructions_per_1k": {
            "conjunction_openers": round(per_k(total.conj_openers, total.words), 3),
            "tricolons": round(per_k(total.tricolons, total.words), 3),
            "passive_probable": round(per_k(total.passive_hits, total.words), 3),
            "contractions": round(per_k(total.contractions, total.words), 3),
            "first_person_singular": round(per_k(total.first_person_sing, total.words), 3),
            "second_person": round(per_k(total.second_person, total.words), 3),
            "numerals": round(per_k(total.numerals, total.words), 3),
        },
        "top_openers": dict(total.openers.most_common(20)),
        "repeated_phrases": {p: n for p, n in total.phrases.most_common(40) if n >= 3},
        "ai_tells": dict(total.ai_tells),
        "hedges": dict(total.hedges),
        "intensifiers": dict(total.intensifiers),
        "per_document": [
            {
                "name": d.name,
                "words": d.words,
                "sentences": d.sentences,
                "mean_sentence_length": round(statistics.mean(d.sent_lengths), 2)
                if d.sent_lengths else 0,
                "ai_tells": sum(d.ai_tells.values()),
            }
            for d in per_doc
        ],
    }


# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("corpus", type=Path, help="Directory (or single file) of writing samples")
    ap.add_argument("-o", "--out", type=Path, help="Write the markdown report here")
    ap.add_argument("--json", type=Path, dest="json_out", help="Also write raw numbers as JSON")
    ap.add_argument("--baseline", type=Path,
                    help="Reference corpus to compare vocabulary against")
    ap.add_argument("--per-file", action="store_true", help="Include the per-document table")
    args = ap.parse_args()

    files = collect_files(args.corpus)
    if not files:
        print(f"No readable files in {args.corpus} "
              f"(looking for {', '.join(sorted(SUPPORTED))})", file=sys.stderr)
        return 1

    per_doc = []
    for path in files:
        text = load_document(path)
        if len(words_of(text)) < 20:
            print(f"skipping {path.name}: under 20 words", file=sys.stderr)
            continue
        per_doc.append(measure(path.name, text))

    if not per_doc:
        print("Nothing left after filtering short files.", file=sys.stderr)
        return 1

    total = merge(per_doc)

    baseline_counts = None
    if args.baseline:
        base_files = collect_files(args.baseline)
        if not base_files:
            print(f"No readable files in baseline {args.baseline}", file=sys.stderr)
        else:
            baseline_counts = merge(
                [measure(p.name, load_document(p)) for p in base_files]).word_counts

    report = build_report(total, per_doc, baseline_counts, args.per_file)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(report, encoding="utf-8")
        print(f"wrote {args.out}", file=sys.stderr)
    else:
        print(report)

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(to_dict(total, per_doc), indent=2), encoding="utf-8")
        print(f"wrote {args.json_out}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
