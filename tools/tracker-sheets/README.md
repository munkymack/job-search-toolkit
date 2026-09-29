# Tracker option A: Google Sheets or Excel

The simple option. One row per application, 18 columns, three dropdowns that keep your data clean.

## Setup (5 minutes)

1. Create a new Google Sheet or Excel file called `Applications`.
2. Import `applications-template.csv`, or paste its one header line into row 1.
3. Freeze row 1.
4. Add data validation (dropdown lists) to these columns. Typing free text into them is how trackers rot.

| Column | Allowed values |
|---|---|
| Seniority | Your own set, for example: entry, mid, senior, lead, manager, director |
| Channel | warm_connection, referral, recruiter, cold_application |
| Stage Reached | applied, screen, interview, final_round, offer |
| Outcome | rejected, no_response, withdrawn, declined, hired (leave blank while open) |
| Fit Rating | 1, 2, 3, 4, 5 |

5. Format Date Applied, First Response Date, and Last Touch as dates (YYYY-MM-DD).
6. Set Notes to wrap text.

## The columns

| Column | Meaning |
|---|---|
| Company, Role | Exactly as on the posting |
| Seniority | Level of the role |
| Channel | How this application got in (never guessed, no default) |
| found_on | Where you spotted the posting (a board, LinkedIn, the company site) |
| Contact Person | Who got you in. Only for warm_connection and referral. |
| Fit Rating | Your 1 to 5 read before applying |
| Stage Reached | Furthest stage that has actually happened. Forward only. |
| Outcome | Blank while open. Set when it ends. |
| Date Applied | The day it went out |
| First Response Date | First reply or decision, including an automated rejection. Not an "application received" email. |
| Last Touch | The date this row was last written. Bookkeeping only. |
| Next Action | What's next and its date |
| Notes | Append-only, one dated line per event |
| Resume File, Cover Letter File | Exact filenames sent |
| Source URL | The posting link |
| jd_file | Filename of the captured posting in `jds/` |

Full field rules are in `skills/log-application.md`. Read them once. They exist because each one was a real data-quality mistake.

## How the AI fits in

It doesn't write to the sheet. It produces the row or the changed fields, and you paste them in. That means nothing in your tracker changes unless you changed it. Every skill that touches the tracker (log-application, pipeline-sweep, draft-followup) works by you pasting rows into the AI and pasting its output back.

To give the AI your open rows for a sweep: filter Outcome to blank, select all, copy, paste into the chat. It reads tab-separated text fine.

## A useful second view

Add a tab that filters on Outcome = blank and sorts by Date Applied, oldest first. That's your pipeline-sweep worklist.

## What to look at weekly

- Response rate by Channel. This is the number that tells you where to spend time.
- Rows at `applied` for 14 or more days with no First Response Date.
- Rows with no Next Action.

## Status

New for this package. The columns match the Notion tracker schema this system was built on, minus two optional referral fields that didn't generalize. The sheet itself hasn't been battle-tested, but the field rules have.
