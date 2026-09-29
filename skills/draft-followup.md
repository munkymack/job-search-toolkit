# Skill: draft-followup

Turns "this application went quiet" into an actual message. Drafts only. It never sends.

## Why this exists

Follow-ups get skipped because writing them feels like begging. This one grounds the message in what you actually submitted, so it reads like a person checking in and not a form letter. It picks up where pipeline-sweep stops: the sweep reports silence and refuses to draft, this drafts and refuses to touch your tracker.

## When to use it

After a pipeline-sweep, or directly: "draft a follow-up for X." Never for a closed application (Outcome set).

## What you need

- The application's tracker row
- The resume and cover letter you actually sent (upload or paste them)
- The captured JD, if you have it
- `templates/outreach-templates.md`, the follow-up section

## The recipient logic

Two separate questions.

**Who to send it to.**
- Contact Person is set: that's the recipient.
- Contact Person is blank but Stage Reached is past `applied`: a real person has already talked to you. Ask who to address it to.
- Contact Person is blank and Stage Reached is still `applied`: **flag, don't draft.** This covers cold applications. Never invent a hiring manager or recruiter name. Never draft to a generic careers inbox. A message nobody reads isn't a follow-up.

**Which voice.**
- Stage Reached past `applied`, any channel: Case 1, post-conversation silence.
- `warm_connection` or `referral`: Case 2, the relationship matters more than this one application.
- `recruiter`: Case 3, short, about availability. Recruiters screen for placeability, not enthusiasm.

## The cap

Two follow-ups per application, maximum. Check Notes for earlier entries that say "follow-up sent" or "followed up." If two are recorded, say so and don't draft a third. A third unanswered follow-up costs more than it can return. If the notes are ambiguous about whether one went out, say so instead of guessing.

## Grounding

Only claims that appear in the materials you sent may appear in the follow-up. No new accomplishments, no reframing, nothing pulled from your story blocks that wasn't in what shipped. A follow-up that introduces a claim the reader never saw reads like a different candidate than the one they screened.

If the file paths in your tracker are stale and you can't find the real resume, say so and ask. Drafting from the wrong document is worse than drafting from none.

## Paste-ready prompt

```
Draft a follow-up for one application. Today's date: [YYYY-MM-DD].

RULES
- Draft only. I send it myself.
- Recipient: use the Contact Person on the row. If it's blank and Stage Reached is still "applied," STOP and tell me it's a cold application with no one to write to. Never invent a name. Never address a generic careers inbox. If it's blank but Stage Reached is past "applied," ask me who to address.
- Voice by case: (1) I've spoken with someone and silence followed, (2) referral or warm connection, (3) recruiter. Use the matching template from my outreach templates file, but write a real draft, not a fill-in-the-blank swap.
- Check the Notes. If two follow-ups are already recorded ("follow-up sent" / "followed up"), say so and do not draft a third. If the notes are ambiguous, say that.
- Only claims that appear in the resume and cover letter I actually sent may appear in the message. No new accomplishments.
- No call to action beyond leaving the door open. No "I'd love to pick your brain." No "circling back." No "hope this finds you well."
- Plain text, subject line included, in a fenced code block. Under 100 words.

After the draft, run the cleanup-pass on it without telling me. Then ask whether it went out. If yes, give me the Notes line to log: "[today]: follow-up sent to [name]."

THE ROW:
[paste]

WHAT I SENT:
[paste resume and cover letter, or say they're in the project]
```

## Rules to keep

1. Drafts only. Never send.
2. Never draft for a closed application.
3. Never invent a recipient.
4. Only claims from the materials actually submitted.
5. Two follow-ups maximum per application.
6. Silence is computed the same way pipeline-sweep computes it, never from Last Touch.
7. Run the cleanup-pass on every draft.

## Differences from the Claude Code version

The Claude Code version read the tracker and the resume files itself. Here you supply both. It also handed the confirmed send to log-application, so one skill writes to the tracker. Keep that separation: this skill drafts, log-application records.
