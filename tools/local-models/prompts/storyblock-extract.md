You are extracting factual records from a piece of professional writing. You are not
writing marketing copy and you are not improving anything. Extract only.

Source file: {filename}

Read the excerpt below and pull out every distinct piece of work it describes. For each
one, fill in this exact structure. Use the source's own words wherever possible.

---
BLOCK
client_or_employer:
project:
role:
problem:
what_i_did:
result:
metric:
constraints:
collaborators:
timeframe:
verbatim_quote:
confidence:
---

Field rules, follow them exactly:

- `problem` is the business situation before the work existed. If the excerpt does not
  state one, write `NOT STATED`. Do not infer it.
- `result` is what changed after. If the excerpt does not state one, write `NOT STATED`.
- `metric` is numbers only: percentages, dollar figures, volumes, timeframes, headcount.
  Copy them exactly as written, including the units. If there are none, write `NONE`.
- `verbatim_quote` is one sentence copied character-for-character from the excerpt that
  best evidences the block. Do not paraphrase it. Do not clean it up.
- `confidence` is HIGH if every field came straight off the page, MEDIUM if you connected
  two nearby statements, LOW if you are mostly guessing. Be harsh with yourself here.
- `constraints` covers budget, timeline, legal or brand review, stakeholder friction, or
  technical limits. Write `NOT STATED` if absent.

Hard rules:

- Never invent a number. Never round one. Never convert one.
- Never write an adjective that is not in the source. No "successful," no "significant,"
  no "impactful."
- If the excerpt contains no describable work at all, output exactly `NO BLOCKS` and stop.
- Output only the blocks. No preamble, no summary, no closing remarks.

Excerpt:

{document}
