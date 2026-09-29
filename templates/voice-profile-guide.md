# Building your voice profile

A written profile of how you actually write, specific enough that another AI can reproduce it. Not "casual but professional." Rules, patterns, and quotes.

## Why bother

Without it, everything an AI drafts for you converges on the same smooth, agreeable, slightly promotional voice. Recruiters and hiring managers have read a lot of it by now. A voice profile is how your cover letters sound like one person wrote them, and that person is you.

## The evidence hierarchy (this is what makes it work)

Not all samples count equally.

**Primary evidence: your own unedited composition.** Emails you wrote, an About Me you wrote, notes, a long message to a friend, a blog post, a LinkedIn post you drafted yourself, rules you wrote about your own writing. High confidence.

**Secondary evidence: AI-drafted, then edited and approved by you.** Cover letters you had an AI write and you tweaked. Reflects your taste in the final cut, not your raw sentence habits. Use it only to confirm patterns already seen in primary sources, never to introduce new ones.

If most of your samples are AI drafts, your profile will describe an AI's voice with your edits on top. Go find some primary writing, even if it's messy.

## The process

### 1. Collect 5 to 15 samples

Mix contexts if you can: something formal, something casual, something explanatory, something personal. Longer is better than shorter. Paste them into one file per sample.

Label each one PRIMARY or SECONDARY.

### 2. Optional: measure first

If you can run Python, `tools/local-models/voice_metrics.py` counts what a language model can't: sentence length and its spread, how you open sentences, contractions, hedges, punctuation rates, repeated phrases. The output goes to your AI assistant as evidence. This is the strongest single input you can give it.

### 3. Run the extraction

```
I'm going to give you writing samples, each labeled PRIMARY (my own unedited writing) or SECONDARY (AI-drafted, then edited and approved by me). Build a voice profile from them.

RULES
- Every rule you write must trace to a quote from a sample. Show the quote.
- A pattern that appears once is an OUTLIER, not a rule. Flag it as one.
- Only use SECONDARY samples to confirm patterns already found in PRIMARY ones.
- Do not use adjectives like "casual," "professional," "engaging," or "authentic." Describe what's on the page.
- If I include a metrics file, treat its numbers as ground truth. Say where the numbers contradict your impression.

SECTIONS
1. Voice summary (5 sentences, concrete)
2. Core writing rules (things I do consistently)
3. Sentence and rhythm patterns (length, variation, fragments, how paragraphs end)
4. Vocabulary and phrasing (words I reach for, words I never use)
5. Structure and formatting (how I organize, where I use lists, how I open and close)
6. Personality and delivery (humor, stance, how I handle praise and criticism on the page)
7. What I never sound like (with quotes of the closest I ever came)
8. Signature patterns (recurring moves that are mine)
9. Before and after: three examples of a generic sentence rewritten in my voice
10. A replication prompt: one block I can paste into any AI to make it write as me, with hard bans and signature moves

SAMPLES:
[paste, each labeled PRIMARY or SECONDARY]
```

### 4. Ask what the evidence contradicts

This is the step that produces something new.

```
Here are the rules I say I follow about my own writing: [paste]. Compare them with the profile and the metrics. Where does my actual writing contradict what I say I do?
```

For example, a rule that bans a punctuation mark, when measurement shows that mark appearing at a steady rate in writing you consider good. That's a real tension worth resolving. You either change the rule or change the writing. Only measurement or a close read surfaces it.

### 5. The register point

You don't have one voice. One worked profile separated three registers with different rules: telegraphic notes to oneself, longer narrative prose, and audience-facing deliverables (cover letters, outreach), which got the strictest treatment. Decide which register your job materials use, and write the replication prompt for that register. Applications shouldn't sound like your diary or like your Slack messages.

### 6. Test it

```
Using the replication prompt, write a 120-word note introducing myself to a hiring manager at [company]. Then list every choice you made that came from the profile.
```

Read it out loud. If no human would say it, or you wouldn't, find the rule that produced that sentence and fix or delete it. Then repeat with a second, different task. Two or three rounds is normal.

## What good looks like

- Rules are testable ("opens with the reader's problem," not "engaging")
- Every rule has a quote
- The profile includes what you never do, not just what you do
- The replication prompt is one paste-ready block

## Keep it alive

When you correct the AI on how something sounds, that's a voice lesson. `skills/capture-lessons.md` files it into your writing rules. Rebuild the full profile if your writing changes a lot, or once after your first ten applications when you have real data on what landed.

## How it connects

- Feeds `skills/cleanup-pass.md` (your sample beats the generic rules)
- Feeds every cover letter and message
- Lives in your project as `voice-profile.md`. Paste the short replication prompt into the project instructions too, since instructions bind more reliably than a file the model may or may not retrieve.
