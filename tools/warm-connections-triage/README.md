# Tool: warm-connections triage

Find the people in your LinkedIn network who could actually help, using your own LinkedIn data export and about an hour of clicking.

## Why this exists

Most senior roles fill through people, not job boards. You already know hundreds of people, but LinkedIn's own interface makes it miserable to review them all at once. This tool loads your entire connection list into one fast table so you can mark each person Warm or Skip, then export the warm ones as a clean file.

"Warm" means someone you could message tomorrow without it being weird: former colleagues, people who've seen your work, people who'd remember your name. It does not mean anyone with a good title.

**Fair warning.** The first pass through a big list is tedious. Budget an hour, do it in one sitting, and be strict. A warm list of 200 you'll never message is worse than 40 you will.

## What you need

- A modern browser (Chrome, Firefox, Safari, Edge)
- Your LinkedIn `Connections.csv` export
- No install, no server, no internet connection while using it

## Step 1: Export your connections from LinkedIn

1. On LinkedIn: your profile photo, then **Settings & Privacy**, then **Data privacy**, then **Get a copy of your data**.
2. Choose **Want something in particular?** and tick **Connections**. (LinkedIn moves these menus around now and then. If you can't find it, search "export connections" in their help.)
3. Request the archive. LinkedIn emails a download link, often within minutes and sometimes up to a day. It arrives as a zip.
4. Unzip it and find `Connections.csv`.

The file starts with a few "Notes:" lines before the column headers. The tool skips them.

## Step 2: Triage

1. Open `connection-triage.html` in your browser (double-click it).
2. Click **Load Connections.csv** and pick your file.
3. Click the button in the Tier column to cycle a person: blank, then **Warm**, then **Skip**, then blank.
4. Use the search box (name, company, or title) and the tier filter to work through it. "Unreviewed" is the filter that shows what's left.
5. Sort by Company A to Z to spot clusters at your target companies. Sort by Recent first if you'd rather start with fresh relationships.

Your marks save automatically in your browser (local storage), and so does the loaded connection list, so you can close the tab and come back. Loading a new CSV replaces the list but keeps your marks for anyone still in it.

Rows with no profile URL are skipped and counted in the progress line.

## Step 3: Export

Click **Export N Warm**. You get `warm-connections.json`, an array of objects with:

`first_name, last_name, full_name, linkedin_url, email, company, position, connected_on (ISO date), relationship_tier ("warm"), intro_eligible (true)`

Move it into your project folder.

## Privacy: read this before you upload anything

The export contains other people's names, employers, job titles, and sometimes emails. Before you upload it to an AI assistant:

- Delete the `email` values (or the field) if you don't need them. Nothing in the workflow requires them.
- Decide whether you're comfortable with your network sitting in your AI account. If not, use the "companies only" version: paste just the company and position columns, with names removed, to find where your network overlaps your target list, then look up the people yourself.

## Step 4: Use it

See `workflows/warm-network-mining.md`. In short: cross the warm list against your target companies and against each role you're applying to, find who's worth a message, and draft outreach using `workflows/linkedin-outreach.md`.

## How it works, if you want to change it

It's one HTML file with no dependencies. The CSV parser handles quoted fields, escaped quotes, and commas inside job titles. Tier marks are stored in `localStorage` under `lc_tiers_v1`, keyed by profile URL, and the connection list under `lc_conns_v1`. The export builds the JSON in the page and hands it to the browser as a file, so nothing leaves your machine.

## Status

This version loads a LinkedIn CSV in the page, with no data baked in. The CSV parser and load path were tested with a sample LinkedIn-format file (quoted commas, quoted quotes, preamble lines, a row without a URL). The tier buttons, filters, and export weren't re-tested in a browser after the CSV change. Try it with your real export and check the first ten rows look right.

## Not included

An n8n workflow prompt for feeding the warm list into an automation. It was written and never used. If you run n8n, `warm-connections.json` is a plain array and any read-file-then-split node will take it.
