# Skill: capture-lessons

At the end of a working session, file the corrections you made so you don't make them again.

## Why this exists

You correct the AI, it does better for the rest of that chat, and the lesson evaporates. Next chat, same mistake. Rules you write down once and put in your project files stop the repeat.

## When to use it

- At the end of a real working session, when you're about to close the chat.
- When you say "capture that" right after a correction.
- Skip it on short sessions with nothing corrective in them.

In the Claude Code version this ran automatically as a session wound down. Chat assistants won't trigger it on their own, so it's a habit: before you close a session where you corrected things, paste the prompt.

## Where lessons go

Sort every lesson into one of three files before you write anything.

| The lesson is about | File |
|---|---|
| **Voice.** Word choice, sentence rhythm, tone, AI-sounding patterns, how a line sounds read aloud. | `writing-rules.md` |
| **Craft.** How a document is put together: structure, framing, what claims go where, what to cut. | `craft-rules.md` |
| **Working style.** How you want the AI to work with you: process, verification, when to ask, how to deliver. | Your project instructions |

The test: does the rule change how a sentence *sounds*, or how a document is *put together*? First is voice. Second is craft. A process lesson is neither. Misfiling shows up later as the wrong kind of rule in the wrong place.

**Working-style changes to your project instructions are proposed, never auto-applied.** The instructions govern everything else. You approve each change.

## What qualifies

- A correction to something the AI wrote: "no," "cut that," "that's backwards"
- A reversal where you overrode a choice
- A pattern it got wrong more than once in the session
- A confirmation, but **only** if you endorsed something it was unsure about or would have reversed on its own. Ordinary approval isn't a signal. "This is solid" is not a rule.

A lesson has to be reusable across sessions and general enough to apply to at least two future tasks. Not one-off ("use this metric in this letter"). Not role-specific. Not already in your files.

## Paste-ready prompt

```
Run capture-lessons on this session.

Step 1. Read my writing-rules.md, craft-rules.md, and project instructions so you know what's already covered. Do not restate anything already there, even loosely.

Step 2. Scope check. Tell me if the early part of this conversation is no longer visible to you, so I know the review isn't a full sweep.

Step 3. Scan for: corrections I made, choices I reversed, patterns you got wrong more than once, and confirmations of non-obvious choices (ordinary approval doesn't count).

Step 4. Keep only lessons that are reusable, general enough to apply to two or more future tasks, and not already covered. Drop one-offs and role-specific framing.

Step 5. Sort each survivor:
- VOICE (how it sounds) -> a line for writing-rules.md
- CRAFT (how it's put together) -> a line for craft-rules.md
- WORKING STYLE (process, verification, delivery) -> a proposed line for my project instructions

Step 6. Write each rule as one short declarative line. No explanation, no hedging. If a new rule is close to an existing one, propose a merged, sharper version instead of a near-duplicate. Never propose deleting a rule.

Output the lines to paste, grouped by file. Put working-style lines under "PROPOSED, needs my approval."

If nothing qualifies, say "Nothing new this session" and stop.
```

## Housekeeping

These files only grow. Once a file passes about 150 lines, or one section passes about 12 rules, run a consolidation pass: ask the AI to merge near-duplicates and flag contradictions, then review the result yourself before replacing the file. Never let it delete rules unsupervised.

## Rules to keep

- Never capture praise.
- Never write working-style lessons into your instructions without approval.
- Don't run it twice on the same material.
- Don't record what you decided not to capture.
