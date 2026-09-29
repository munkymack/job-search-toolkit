# Tracker option B: Notion

The tracker this workflow was built on. A Notion database with one page per application, plus a small Python client so scripts (and you) read and write it safely.

Pick this if you already live in Notion and you're comfortable running Python. Otherwise use `tools/tracker-sheets/`. The columns are identical.

## What you get

- A database with 18 properties and a page body that holds the captured job description
- `notion_tracker.py`, a standard-library-only Python client with helpers for the common operations: schema check, query, find by company, create a page, update properties, and append to Notes without overwriting
- Schema verification before any write, so a renamed or deleted property stops the script instead of writing data into the wrong shape

## Setup

### 1. Create the database

In Notion, create a full-page database called **Applications** with these properties. Names must match exactly.

| Property | Type | Values |
|---|---|---|
| Company | Title | |
| Role | Text | |
| Seniority | Select | your own set, e.g. entry, mid, senior, lead, manager, director |
| Channel | Select | warm_connection, referral, recruiter, cold_application |
| Contact Person | Text | |
| Fit Rating | Number | 1 to 5 |
| Stage Reached | Select | applied, screen, interview, final_round, offer |
| Outcome | Select | rejected, no_response, withdrawn, declined, hired |
| Date Applied | Date | |
| First Response Date | Date | |
| Last Touch | Date | |
| Next Action | Text | |
| Notes | Text | |
| Resume File | Text | |
| Cover Letter File | Text | |
| Source URL | URL | |

`found_on` and `jd_file` live inside the page body in a "Capture metadata" toggle rather than as properties. You can add them as properties too if you'd rather; the client won't care.

### 2. Create an integration and connect it

1. Go to Notion's integrations page and create an internal integration. Copy its secret.
2. Open your Applications database, choose Connections from the page menu, and add the integration. Without this, the API can't see the database.
3. Copy the database ID from the URL: the 32-character string before the `?v=`.

### 3. Set two environment variables

```bash
export NOTION_API_KEY="secret_..."
export NOTION_DATABASE_ID="your-32-character-id"
```

Put them in your shell profile or a `.env` file you load yourself. **Never paste your key into a chat assistant, and never commit it to a repo.**

### 4. Test the connection

```bash
cd tools/tracker-notion
python3 -c "import notion_tracker as nt; nt.check_schema(); print('schema ok', nt.count_pages(), 'pages')"
```

If it raises `NotionError`, the message says what's wrong (missing key, missing property, unreachable database). Fix that before doing anything else.

## Using it with a chat assistant

A chat assistant can't call the API for you. The workflow is:

1. Ask the AI to work out the row or the changed fields (`skills/log-application.md`, `skills/pipeline-sweep.md`).
2. Write the values with the client, or type them into Notion by hand.

Example: creating a page.

```python
import notion_tracker as nt
nt.check_schema()
props = {
    "Company": nt.title("Acme"),
    "Role": nt.rich_text("Senior Product Manager"),
    "Seniority": nt.select("senior"),
    "Channel": nt.select("warm_connection"),
    "Contact Person": nt.rich_text("Jane Doe"),
    "Stage Reached": nt.select("applied"),
    "Date Applied": nt.date("2026-09-29"),
    "Last Touch": nt.date("2026-09-29"),
    "Notes": nt.rich_text("2026-09-29: applied"),
    "Source URL": nt.url("https://example.com/jobs/123"),
}
nt.create_page(props)
```

Example: appending a note without touching earlier ones.

```python
page = nt.find_by_company("Acme")[0]
nt.append_note(page["id"], page, "2026-10-06: recruiter replied, screen scheduled for 10-10")
```

Example: your open applications, for a sweep.

```python
open_pages = nt.query_all({"property": "Outcome", "select": {"is_empty": True}})
for p in open_pages:
    print(nt.get_text(p, "Company"), nt.get_select(p, "Stage Reached"), nt.get_date(p, "Date Applied"))
```

## Rules the client encodes

- **Notes is append-only.** `append_note` reads the current value and writes the concatenation in one call, so it never assumes what's there.
- **Schema is checked before writing.** A changed database stops the script. It never adapts silently.
- **One page per operation, matched by ID.** Never a name-based bulk update.
- After any write, re-fetch the page and confirm it landed as intended. There's no undo for a Notion property.

## Status

A generalized version of the client used in the Claude Code version, with the hardcoded database ID replaced by the `NOTION_DATABASE_ID` variable and two optional referral properties that didn't generalize removed from the required list. The import and the pure helper functions were checked. It was **not** run against a live Notion workspace in packaging, so treat your first `check_schema()` as the real test.
