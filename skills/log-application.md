# Skill: log-application

Keep one row per application, and only log what's true.

## Why this exists

An application that isn't logged is invisible to everything downstream: follow-ups, weekly review, the numbers that tell you which channel is working. A half-full tracker lies worse than an empty one.

## The rule that matters most

Tailoring is not applying. Log an application only when you confirm it was sent.

## Pick your tracker

Two options. Pick one. The columns are identical.

| | Google Sheets / Excel | Notion |
|---|---|---|
| Setup time | 5 minutes | 30 to 45 minutes |
| The AI can update it directly | No. It gives you the row, you paste it. | No. Scripts do it, the AI drafts the values. |
| Best for | Most people | People who already live in Notion and are comfortable running Python |
| Files | `tools/tracker-sheets/` | `tools/tracker-notion/` |

Either way, the AI is the thinking layer. It figures out what the row should say. You or a script do the writing. That's a real difference from the Claude Code version, where the AI wrote to the database itself, and it's a good one: nothing changes in your tracker unless you did it.

## Field rules (both trackers)

**Company, Role.** From the conversation.

**Date Applied.** Today, unless you say otherwise. Never let the AI guess today's date. Tell it.

**Seniority.** Pick a set that fits your field, for example `entry`, `mid`, `senior`, `lead`, `manager`, `director`. The AI proposes one, you confirm. Never set silently.

**Channel.** How the application got in. One of `warm_connection`, `referral`, `recruiter`, `cold_application`. No default and never guessed. This is the most valuable column in the tracker, because it tells you which approach actually gets responses. Let your own data tell you.

**found_on.** Where you spotted the posting: LinkedIn, a specific board, the company site. Different question from Channel. A referral can come from a role first seen on LinkedIn. The Channel tells you which approach works. found_on tells you which boards earn your search time.

**Contact Person.** Only for `warm_connection` and `referral`: who got you in. Not who you'd like to talk to.

**Fit Rating.** 1 to 5, or blank.

**Resume File, Cover Letter File.** The exact filenames you sent. Never a guess. A blank is a normal state.

**Source URL.** The posting link.

**Stage Reached.** The furthest stage that has actually happened: `applied`, `screen`, `interview`, `final_round`, `offer`.

- It only moves forward. A rejection after an interview leaves Stage Reached at `interview`. Collapsing "how far it got" into "how it ended" hides the data you need.
- Jump straight to the stage you reached. Screens often go unlogged, so `applied` can go straight to `final_round`.
- Reached, not scheduled. A booked interview is not a reached interview. Put the booking in Notes and Next Action and leave Stage Reached alone.
- Rounds that aren't on the ladder (portfolio review, take-home, work sample) don't advance it. Record them in Notes.

**Outcome.** Blank while open. Set only when it ends: `rejected`, `no_response`, `withdrawn`, `declined` (you turned down an offer), `hired`. `hired` and `declined` both require Stage Reached = `offer`. If Outcome is already set, stop and ask before changing it. Marking `no_response` is your call, never the AI's. It can tell you how many days it's been. You decide.

**First Response Date.** Set once, when blank. A response is a reply or a decision: an interview invite, a recruiter reply, a request for more material, a rejection, including an automated form rejection. Catching a three-day auto-reject is half the point of this column. Not a response: an automated "we received your application" or an ATS status page change.

**Last Touch.** The date you wrote to the row. It records bookkeeping, not contact. Never use it to measure silence.

**Next Action.** What's next and its date, like `follow up 2026-10-06`. Clear it when the application closes.

**Notes.** Append-only, one line per event: `YYYY-MM-DD: what happened`. Date each entry to the event, not to the day you logged it. Keep your own wording on feedback and stated reasons.

## Paste-ready prompt: new application

```
Act as my application tracker clerk. Today's date: [YYYY-MM-DD].

I just sent an application. Produce the tracker row, following these rules:
- Ask me for anything you can't get from what I tell you. Never fabricate.
- Propose Seniority and ask me to confirm. Never set it silently.
- Channel has no default. Ask if I haven't said. Options: warm_connection, referral, recruiter, cold_application.
- Ask for found_on and Source URL. Accept "skip".
- Ask for Contact Person only if Channel is warm_connection or referral.
- Ask for Resume File and Cover Letter File names. Blank is fine. Never guess.
- Stage Reached = applied. Outcome blank. First Response Date blank. Last Touch = today. Notes = "[today]: applied".

Output the row as [CSV line / a table with one row], in this column order:
Company, Role, Seniority, Channel, found_on, Contact Person, Fit Rating, Stage Reached, Outcome, Date Applied, First Response Date, Last Touch, Next Action, Notes, Resume File, Cover Letter File, Source URL, jd_file

Here is what I applied to:
[company, role, anything else you know]
```

## Paste-ready prompt: update an existing application

```
Act as my application tracker clerk. Today's date: [YYYY-MM-DD].

Here is the current row:
[paste the row]

Here is what happened:
[what happened, and when]

Apply these rules and give me only the changed fields plus the new Notes line:
- Stage Reached moves forward only, to the furthest stage actually reached. A scheduled interview is not a reached interview.
- Outcome: if it is already set, stop and ask me before changing it. Never mark no_response yourself. Tell me how many days it has been since real contact and let me decide.
- hired and declined require Stage Reached = offer. If that's not true, ask.
- First Response Date: set only if blank, and only for a reply or decision, including an automated rejection. Not for an "application received" email.
- Last Touch = today.
- Next Action: update it, or clear it if this closed the application.
- Notes: give me one new line dated to the event. Don't rewrite earlier lines.
- If what I tell you contradicts the row, ask. Don't overwrite.
```

## Backfilling an old application

Tell the AI it's a backfill. It changes three things: ask for the real Date Applied (never default to today), write one dated Notes line per known event instead of a single "applied" line, and set Stage and Outcome to current reality.

## Rules to keep

1. Never fabricate a field. Ask.
2. Stage Reached moves forward only.
3. Notes is append-only.
4. Touch one application per operation.
5. Get today's date from you, not from the model.
6. Log only after you confirm the application went out.

## Differences from the Claude Code version

The Claude Code version wrote to Notion through `scripts/notion_tracker.py` and re-fetched the page after every write to verify it. The Notion option here keeps that script (see `tools/tracker-notion/`). The Sheets option has no verification step, so read the row back after you paste it. It also had two optional referral fields that didn't generalize. Those are dropped.
