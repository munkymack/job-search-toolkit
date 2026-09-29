# Target companies: template

The proactive layer of the search. Companies worth wanting whether or not they have a posting up. It gives Monday's targeting and Wednesday's outreach a spine.

Not the same as a scraper seed list or your warm-connections list. This is *employers you'd want*, tiered by how hard you're chasing them.

## The structure

```markdown
# Target companies

**Filter applied:** [your location and work-mode constraints, plus any role-content minimum]
**Last reviewed:** [date]. Review monthly, ideally at a Friday retro.

**Standing caveats:** [anything about the market that changes how you weight this,
e.g. recent layoffs, mergers, hiring freezes, RTO mandates in your sector.
Date them.]

## Tier A: chase now (aim for about 10 to 15)
Career pages checked every Monday. These drive outreach. You want the job here
whether or not a req is live.

| Company | Why here | What they'd hire me as | Who I know | Status |
|---|---|---|---|---|

## Tier B: strong, work steadily
| Company | Why here | What they'd hire me as | Who I know | Status |

## Tier C: backup and long shots
| Company | Why here | Notes |
```

Tags worth using in a column: work mode (`[remote]`, `[hybrid]`, `[onsite]`) and location. Note that "remote" means different things by year and company, so re-verify per role.

## How to build it

Don't start from nothing. Ask the AI for candidates, then cut hard.

```
Here is my About Me, my constraints, and my positioning. Propose 30 companies I should consider, grouped into three tiers.

For each: why it fits me specifically (one line), what role they'd likely hire me into, and one honest reason it might not work.

Rules:
- Only include companies you are confident exist and are still operating. Mark anything you're unsure about as [verify].
- Don't pad with famous names. Include smaller and less obvious companies that match my constraints.
- Flag any company with recent layoffs, restructuring, or acquisition news you know of, with the date. If your information may be out of date, say so.
- Do not invent facts about their teams, headcount, or open roles. I'll verify with their career pages.
```

Then verify each Tier A company yourself: is it operating, is it hiring your function, who's on the team. The AI's knowledge of specific companies goes stale.

## How it connects

- Monday: check Tier A career pages.
- Wednesday: pick one person at a Tier A or B company to message.
- `workflows/warm-network-mining.md`: cross your warm list against this file.
- `recruiter-screen`: reads it for context on the company and any warm contacts there.

## A second, wider list (optional)

Consider keeping a broader map as well, unfiltered by location and not tiered, as a prospecting pool for weeks when the main pipeline runs thin. Companies graduate from the wide list into a tier when they earn a real look. If your field has an equivalent set (agencies, consultancies, staffing firms, a class of startup), keep it as a separate file. Don't bloat the main one.
