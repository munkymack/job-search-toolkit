# Workflow: warm-network mining

Turn your LinkedIn connection list into a short, ranked list of people worth writing to. Uses the output of `tools/warm-connections-triage/`.

## Why this exists

Warm connections are the highest-value channel in a search, and they're the one most people never use systematically. You know someone at half your target list. You've forgotten. The triage tool sorts the whole network once. This workflow uses the result week after week.

## Two lists, not one

Keep two, and the distinction matters.

1. **The full warm list** (`warm-connections.json` from the triage tool). Everyone you'd be comfortable messaging. Wide. Mostly dormant.
2. **The activation list.** A short list of people who have actually helped, or who are connected to real applications: someone who referred you, someone who passed your resume along, a former colleague who was in the loop when a role went quiet. Small. Specific. Each with a status: fresh (never asked), used once, ghosted, active.

The full list is your map. The activation list is who you write to *this week*. Build the second one by hand from your tracker's Contact Person column plus your memory. Be strict: an inflated list (router-type contacts, aspirational names, self-references) is worse than a short honest one.

## The tool's limit, stated plainly

LinkedIn's export gives each connection's **current** company and position, as of the export. It doesn't show where they used to work. So "who do I know at Company X" finds current employees only. Former employees, who are often the more candid source, need a manual look.

## Setup

- `warm-connections.json` (from the triage tool)
- Your target-companies file (`templates/target-companies-template.md`)
- Optional: your activation list

Strip the `email` field from the JSON before uploading, if you can. See the privacy note in the triage tool README.

## Workflow A: weekly, by target company

```
Below is my list of warm connections (JSON) and my target companies file.

1. For each Tier A and Tier B target company, list every warm connection whose current company matches. Match loosely on company names (Google = Google LLC = Alphabet). Show name, position, connected_on date.
2. For each match, say how recent the connection is and whether their position is near my target function.
3. Rank the top 5 people to contact this week, with one line each on why.
4. List target companies where I have no current-employee connection.
5. Say what you can't know from this data: former employees, how well I actually know each person, and whether they'd still recognize me.

Do not guess about relationships beyond what's in the data.

[paste JSON]
[paste target companies]
```

## Workflow B: per role you're about to apply to

```
I'm about to apply to [ROLE] at [COMPANY]. Here is my warm-connections list.

1. Who works at [COMPANY] now? Show name, position, connected_on.
2. Who works at a company that is a known competitor, partner, or former employer of [COMPANY]'s team, if you can tell from the JD? Show why.
3. Who would be worth asking a narrow question ("is the team hiring, what's it like") before I apply, and who should I ask for a referral? Say which is which and why.
4. What's the risk of asking each one?

I will decide who to contact. Don't draft messages yet.
```

Then draft with `workflows/linkedin-outreach.md`.

## Workflow C: monthly refresh

1. Export LinkedIn connections again.
2. Load the new CSV in the triage tool. Your earlier Warm and Skip marks persist for anyone still in it.
3. Filter to Unreviewed and Recent first. Only new connections need triage.
4. Re-export.

## Rules

- A warm list you never message is decoration. If five people go untouched for a month, tighten the list.
- Referral bonuses are real at many companies. If the person feels you're a fit, they may get one, which is a fair thing to name.
- Never use a warm contact for a role you wouldn't take.
- Log every application that came through a connection with Channel = `warm_connection` or `referral`, and the Contact Person. That's how you learn what works.
