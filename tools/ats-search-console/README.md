# Tool: ATS search console

Search the applicant tracking systems directly, one board at a time, for roles that haven't hit the big job sites yet.

## Why this exists

Most companies post to an ATS (Greenhouse, Lever, Ashby, Workday and so on) and only sometimes syndicate to LinkedIn or Indeed. Google indexes those ATS pages. A search scoped to one ATS, with your titles and locations, finds roles the aggregators miss or bury.

The console builds those searches for you. You type your job titles and locations once and get a live Google link per board. It makes no network calls itself. It only builds links.

## How to use it

1. Open `ats-search-console.html` in your browser.
2. Enter your titles, comma separated. Each becomes an exact-match phrase.
3. Enter your locations, comma separated. Include "Remote" if you want it. Leave blank for no location filter.
4. Pick a time window (past week is the right default for a weekly pass) and Full-time or Freelance/contract.
5. Click **Search** on each board. Skim the first page of results. Open anything that looks live.

Your titles and locations are remembered in your browser between visits.

**Weekly rhythm:** once a week, past-week window, all 13 boards. About 20 minutes. Anything worth pursuing goes to capture-jd right away, because listings vanish.

## The rules built into every query (and why)

- **One `site:` per query, never inside parentheses.** Google silently drops the host filter when `site:` sits inside a parenthesized OR group. `(site:a OR site:b)` returns results from everywhere. Boards that span two hosts get two entries instead, which is why Greenhouse and Rippling each appear twice.
- **Straight quotes only.** Curly quotes break exact-match search. The console strips curly quotes from what you type. If you copy a query into a document first, check that the quotes didn't curl.
- **Full-time queries carry no "full-time" term.** Requiring it cut Greenhouse results by roughly 90%, because most postings never say it. The trade-off: the full-time list is broader and includes some contract roles. The freelance list is the precise one.
- **Every other OR group is parenthesized**, because Google binds AND tighter than OR, and an unparenthesized group splits the query into independent branches.

## The boards

Greenhouse (two hosts), Lever, Ashby, Workday, Rippling (two entries), BambooHR, Breezy, Gusto, Y Combinator's Work at a Startup, Sequoia, a16z. 13 boards, times two for full-time and freelance.

To add a board, add a line to the `BOARDS` list near the bottom of the HTML file: `{ name: "Display name", host: "the-host.com" }`. Add a `flx` list if that ATS words contract roles differently (Workday does: "contract," "contingent," "temporary").

## When a board goes quiet

If a board returns nothing for weeks, first check the query by pasting it into Google yourself and clicking through a page or two. Then check whether the ATS changed its hostname. ATS vendors do change hostnames. Greenhouse is already listed under two, which is why it has two entries.

## What this is not

It is not a continuous feed. It needs you to run it. The Claude Code version also had a script that polled company job boards automatically and synced new roles into a database. It was left out on purpose: it's hardwired to one set of titles and location rules and would need a rewrite for anyone else. The console is the manual version of the same job, with nothing to maintain.

## Status

Rewritten for this package. The earlier version was hardwired to one set of titles and locations. The query builder was tested in Node against that version's query shapes, including curly-quote cleanup, the Workday clause override, blank locations, and blank titles. It hasn't been clicked through in a browser, so open it once and confirm a Search link opens the Google query you expect.
