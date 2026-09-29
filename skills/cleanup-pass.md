# Skill: cleanup-pass (humanizer + stop-slop)

Strips the tells that make a resume, letter, or message read as machine-written. Run it on anything a human will read before it goes out.

In the Claude Code version this was two separate skills that ran automatically, back to back, on every deliverable:

1. **humanizer**, an open-source skill (MIT) built on Wikipedia's "Signs of AI writing" guide. It catches inflated significance, promotional language, vague attributions, tacked-on -ing phrases, AI vocabulary, negative parallelisms, rule-of-three padding, filler, hedging, and more.
2. **stop-slop-extras**, a small companion adapted from the open-source stop-slop project by Hardik Pandya (MIT). It adds three things humanizer doesn't cover: business jargon, sentence starters that turn into crutches, and a scoring gate.

A chat assistant can't load those skill files, so both are condensed into one prompt below. The full humanizer is worth reading if you want the before/after examples for each pattern. It's on GitHub under the same name.

## When to use it

Every time. On resumes, cover letters, outreach, follow-ups, emails. Don't announce it in the draft. Run it and deliver the cleaned version.

Not needed for internal notes you'll read once.

## The single most useful upgrade: give it a sample of your own writing

If you paste a few paragraphs you actually wrote, the pass matches your habits instead of imposing a generic "human" voice. A real sample beats every rule below, including the dash rule. If your sample uses em dashes, keep them at your rate. Build your voice profile first (`templates/voice-profile-guide.md`) and this pass gets much better.

## Paste-ready prompt

```
Run a cleanup pass on the text below and deliver the clean version.

PRESERVE FIRST
- Every fact, name, number, date, and claim in the source text survives. Never add a fact, number, quote, or detail that isn't in the source. If a vague sentence needs real detail to work, ask me for it or write the plain version.
- If I include a writing sample, match its habits (sentence length, punctuation, vocabulary, quirks). The sample outranks every rule below.

CUT ON SIGHT
- Inflated significance: "a testament to," "pivotal," "plays a key role," "underscores," "marks a shift," "evolving landscape," "setting the stage for."
- Promotional language: "vibrant," "groundbreaking," "renowned," "stunning," "boasts," "commitment to."
- Tacked-on -ing analysis: sentences that end with ", highlighting..." / ", ensuring..." / ", showcasing..." / ", fostering...".
- Vague attribution: "experts say," "industry reports suggest," "observers have noted" with no named source.
- AI vocabulary: additionally, delve, crucial, pivotal, tapestry, testament, intricate, landscape (abstract), foster, garner, showcase, underscore, vibrant, enduring, align with, key (adjective), valuable.
- Copula avoidance: "serves as," "stands as," "boasts," "features" where "is" or "has" works.
- Negative parallelism: "not just X, but Y," "it's not X, it's Y," and closers like "they don't replace it, they extend it." Cut the second clause or the line.
- Manufactured drama: a run of short fragments to fake punch. One short sentence to land a point is fine.
- Aphorism formulas: "X is the currency of Y," "X becomes a trap."
- Rule-of-three padding when the honest count is two or four. Synonym cycling to avoid repeating a word. False ranges ("from X to Y" where there's no scale).
- Filler and hedging: "in order to," "it is important to note," "could potentially," "arguably," "at the end of the day."
- Generic positive closers: "exciting times ahead," "looking forward to what's next." End on the last concrete fact.
- Signposting: "Let's dive in," "here's what you need to know," "what ties this together is."
- Sycophancy and chat leftovers: "Great question," "I hope this helps," "Certainly!"
- Self-graded significance on the writer's own work ("is work a firm rarely allows itself"). State what happened. Skip the verdict on how impressive it is.
- Hyphenated-pair overuse (cross-functional, data-driven, end-to-end) when the plain phrase works.
- Em dashes and en dashes: replace with a comma, colon, period, or split the sentence. [DELETE THIS LINE IF YOUR SAMPLE USES DASHES.]
- Emoji, exclamation points, title case in headings (use sentence case), bold-spam, and bullet lists where prose reads better.

BUSINESS JARGON: replace with plain language
navigate (challenges) -> handle; unpack -> explain; lean into -> accept; landscape -> situation or field; game-changer -> significant; double down -> commit; deep dive -> analysis; take a step back -> reconsider; moving forward -> next; circle back -> return to; on the same page -> aligned.

SENTENCE STARTERS
- Restructure sentences that open with What, When, Where, Which, Who, Why, or How. Lead with the subject or the verb. "What makes this role interesting is..." becomes "This role is interesting because...", or better, name the specific thing.
- Never start a paragraph with "So."

DO NOT FLAG (these are not tells on their own)
Perfect grammar. Formal vocabulary that isn't on the list above. One "however." A salutation or sign-off. One short emphatic sentence. Look for clusters of tells, not single instances. Leave alone anything that reads as a real person: a specific unusual detail, a defensible opinion, uneven rhythm, a self-correction.

SCORE BEFORE DELIVERING (1 to 10 each)
Directness (statements, not announcements) / Rhythm (varied, not metronomic) / Trust (respects the reader) / Authenticity (sounds human) / Density (anything cuttable?).
Under 35 out of 50 total: revise before showing me.

THEN
1. Deliver the final text in a fenced code block.
2. Below it, two lines: what changed and why.
3. Then answer honestly: what would still make this read as AI-written? One line.

TEXT:
[paste]

MY WRITING SAMPLE (optional):
[paste]
```

## Rules to keep

- Meaning survives. The pass changes how it sounds, not what it claims.
- Your own writing sample beats the generic rules.
- The pass is a floor, not a voice. Text with none of these tells can still be flat. If it reads bland after cleanup, the fix is usually more specifics, not more polish.
- Read the result out loud. If no human would say it, rewrite it.
