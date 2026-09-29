# Tool (optional): local-models

Measure your own writing with a script, and optionally extract raw material for story blocks with a model running on your own computer.

**Status up front:** the voice-measurement script works and was run on sample files. The local-model half was set up and timed on one home server but was never run against a real writing corpus. Treat it as untested. Skip the whole folder if you don't have a machine that runs Ollama.

## Why this exists

Two jobs came up: describe your writing voice accurately, and pull accomplishment facts out of a pile of old documents.

The insight that shaped it: **a language model describing your voice cold produces a horoscope.** "Conversational tone, varied sentence length, active voice" is true of everyone. What actually distinguishes a writer is low-frequency signal across a lot of text: how often you open a sentence with "And," how many words per sentence and how much that swings, how many hedges, which function words you overuse. A model reading one chunk can't see that. A script can count it exactly.

So the split is:

| Job | Who does it |
|---|---|
| Measure voice | `voice_metrics.py`, no model, exact numbers |
| Interpret the numbers | Your AI assistant (or you), given the metrics plus 3 or 4 full samples |
| Extract facts for story blocks | A local model into a fixed schema, one chunk at a time |
| Turn those facts into persuasive story blocks | Your AI assistant or you. Never the small local model. |

Why not let the local model write the blocks: persuasive reframing depends on voice, and a small model asked to make a story compelling produces LinkedIn filler.

## Part 1: voice_metrics.py (recommended, no model needed)

Python 3.9+, standard library only. Reads `.md`, `.txt`, and `.docx`.

```bash
mkdir corpus
# put 5 to 15 of your own writing samples in corpus/
python3 voice_metrics.py corpus/ --per-file -o out/voice-metrics.md
```

It measures sentence length and how much it varies ("burstiness"), paragraph shape, punctuation rates, how sentences open, contractions, hedges, intensifiers, probable passive voice, three-item lists, repeated phrases, readability, vocabulary richness, and a set of common AI-writing tells. It makes no quality judgments. Every number is exact.

**Add a baseline for much better results:**

```bash
python3 voice_metrics.py corpus/ --baseline reference/ --per-file -o out/voice-metrics.md
```

`reference/` is writing that is deliberately not yours: generic marketing copy, competitors' blog posts, or a folder of AI drafts of the same briefs. With a baseline it reports what's distinctive about your writing rather than merely frequent. The function-word table is the one to read, because function-word rates are close to unconscious and hold across subjects.

`--per-file` shows whether your voice holds steady across contexts. Variance between, say, work writing and personal writing is a finding by itself.

**Then hand your AI assistant three things:** the metrics file, three or four complete samples, and your existing writing rules. Ask: "What do these numbers contradict in my stated rules?" That framing produces something new. Asking it to describe your voice cold gets you the horoscope.

**Known limits:** passive-voice detection is a heuristic with no part-of-speech tagging, so treat it as directional. Sentence openers get polluted by heavily structured documents (list labels read as sentence starts), so prose samples give cleaner results. Comparing essays to a resume mostly measures the genre gap. Spot-check any number before quoting it.

Checked for this package: run on two sample markdown files, it produced a full report.

## Part 2: ollama_batch.py (optional, untested on real data)

Runs one prompt over a folder of documents against a local Ollama server, chunking long inputs and saving each result to disk so a crash doesn't cost you the run. It talks to Ollama's `/api/generate` directly because chat front ends time out long before a CPU-only machine finishes reading a big chunk.

```bash
# see the plan before committing
python3 ollama_batch.py -p prompts/storyblock-extract.md -i corpus/ -o out/blocks --dry-run

# run it
python3 ollama_batch.py -p prompts/storyblock-extract.md -i corpus/ -o out/blocks \
  -m <your-model> --chunk 1500
```

Set `OLLAMA_HOST` if your server isn't on localhost. Reruns skip chunks that already have output. Failed chunks write a `.error.txt` and the run continues. `ollama_batch.py` imports from `voice_metrics.py`, so keep them in the same folder.

Two prompts are included:

- `prompts/storyblock-extract.md` fills a fixed schema (client, project, role, problem, what I did, result, metric, constraints, collaborators, timeframe, a verbatim quote, and a confidence rating). Rules: never invent a number, never add an adjective that isn't in the source, write NOT STATED instead of inferring. **Sort the output by confidence and read the LOW ones first. That's where the fabrication is.**
- `prompts/voice-observe.md` forces every observation to carry an exact quote from the text. Treat the quotes as the output and the commentary as noise.

**Dry run tested** on sample files for this package (it chunked correctly). It has never been run against a live Ollama server on a real corpus.

## Do you need this?

Honestly, probably not. A chat assistant with a good extraction prompt (see `templates/story-blocks-build-guide.md`) does the story-block job with less setup. The reasons to use the local route: your source documents are sensitive and shouldn't leave your machine, or you have a large corpus and want to avoid pasting it chunk by chunk.

If you only take one thing from this folder, take `voice_metrics.py`. It's the one part where a plain script beats a language model.

## Hardware note

Large models read slowly on CPU-only hardware, and a big corpus can take a long time before any output appears. Start long runs overnight. Keep one large model loaded at a time or the machine swaps and slows to a crawl. If your hardware reads under about 15 tokens per second, use a smaller model or skip this part.
