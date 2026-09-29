# Skill: pipeline-sweep

A pass over every open application. It tells you what has gone quiet, then you tell it what's new.

## Why this exists

Your tracker fills up and you stop looking at it. A sweep forces the question "where does everything actually stand," with real numbers.

Information flows the opposite way from log-application. There, you tell the AI what happened to one application. Here, it tells you what's gone quiet first, and then you respond. Lead with the report, not with questions.

This skill is tracker only. It doesn't draft follow-ups. That's draft-followup.

## When to use it

Weekly (Friday works) or whenever you catch yourself wondering where things stand. Words like "sweep," "what's gone quiet," "what needs chasing."

## What you need

Your tracker exported or pasted: every row with Outcome blank. Closed rows (Outcome set) are out of scope. If you have news on a closed row, like a recruiter circling back to a rejected role, it gets surfaced and you decide, using log-application to reopen it.

## The silence calculation

This is the part people get wrong, so it is spelled out.

Days quiet = today minus the later of:
1. First Response Date if set, otherwise Date Applied.
2. The most recent Notes entry that records real contact **on that entry's own date**: a reply, a call, an interview that happened that day.

An entry does not count as contact if it is:
- **Bookkeeping.** "logged," "corrected," "backfilled." The row was written that day. Nobody talked to anyone.
- **A reference to earlier contact.** How you found the role, who referred you, what a recruiter said last month. It's dated the day you wrote it down, not the day it happened.

If you can't tell, don't count it. Counting a non-contact makes the silence look shorter, and short is the dangerous direction because it hides a stalled application behind a fresh-looking number.

**Never compute silence from Last Touch.** It moves every time the row is written, including for pure bookkeeping, so it understates the gap on the exact number you're about to decide from.

Also flag any row whose Next Action names a date now in the past.

## Paste-ready prompt

```
Run a pipeline-sweep. Today's date: [YYYY-MM-DD].

Below are my open applications (Outcome is blank). Report first, ask second.

For each application, compute days quiet:
- Start from First Response Date if set, otherwise Date Applied.
- Compare with the most recent Notes entry that records real contact ON THAT ENTRY'S OWN DATE (a reply, a call, an interview that happened that day). Use the later date.
- Do NOT count bookkeeping entries ("logged," "corrected," "backfilled") or entries that merely mention earlier contact (how I found the role, who referred me). If unsure, don't count it.
- NEVER use Last Touch.
Give the number of days. "Too early to call quiet" is not a report. "2 days" is.

REPORT, sorted by days quiet, longest first. For each: company, role, Stage Reached, days quiet, Next Action, and whether the Next Action date is overdue.

Then note, without deciding anything:
- Rows quiet long enough that I might want to mark no_response
- Rows with an overdue Next Action
- Rows with no Next Action at all
- Rows with no captured job description (the posting is probably still up now and won't be later)

NEVER mark anything no_response yourself. State the days and let me decide. No cutoff, no "this one's dead," no bulk closing.

After the report, ask what news I have. I'll answer in free form across several applications. For each one with news, give me only the changed fields plus one new Notes line, following these rules:
- Stage Reached: only stages that have actually happened. A booked interview is not a reached interview. Forward only.
- First Response Date: set only if blank, for a reply or decision including an automated rejection. Not for "application received."
- Last Touch: today's date.
- Notes: one line per event, dated to the event.
- Next Action: update or clear it on every row I touch.
A row with no news is not touched at all. No Last Touch bump. Touching every row every sweep turns Last Touch into "date of last sweep" and destroys it.
If news contradicts a row, ask. If it's about a closed row, surface it and stop.

MY OPEN APPLICATIONS:
[paste rows]
```

## Rules to keep

1. Report the days-quiet number before asking anything.
2. Never compute silence from Last Touch.
3. The AI never sets no_response. You decide.
4. Stage Reached reflects what has happened, never what is scheduled.
5. Rows with no news don't get touched.
6. Closed rows are out of scope.
7. Tracker only. No follow-up drafting.

## Differences from the Claude Code version

The Claude Code version read the Notion database itself and verified afterward that row counts hadn't changed. In a chat assistant you paste rows in and paste the changes back. After you apply them, confirm the total row count is what it was. A sweep never creates or deletes rows.
