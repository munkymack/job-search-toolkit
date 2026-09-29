"""
Small Notion client for a job-search Applications database.

Stdlib only. Requires two environment variables:
    NOTION_API_KEY       the secret from your Notion integration
    NOTION_DATABASE_ID   the id of your Applications database

Expected properties are listed in EXPECTED_PROPERTIES below. check_schema()
confirms they all exist before you write anything.
"""

import json
import os
import urllib.error
import urllib.request

def _db_id():
    db = os.environ.get("NOTION_DATABASE_ID")
    if not db:
        raise NotionError("NOTION_DATABASE_ID is not set.")
    return db

EXPECTED_PROPERTIES = {
    "Company", "Role", "Seniority", "Channel", "Contact Person",
    "Fit Rating", "Stage Reached", "Outcome",
    "Date Applied", "First Response Date", "Last Touch", "Next Action",
    "Notes", "Resume File", "Cover Letter File", "Source URL",
}

STAGE_LADDER = ["applied", "screen", "interview", "final_round", "offer"]


class NotionError(RuntimeError):
    pass


def _token():
    token = os.environ.get("NOTION_API_KEY")
    if not token:
        raise NotionError(
            "NOTION_API_KEY is not set. Set it before running anything here."
        )
    return token


def _request(method, url, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {_token()}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        raise NotionError(f"Notion API {method} {url} failed: {e.code} {e.read().decode()}")


def check_schema():
    """Confirm the database still has the expected properties. Call this
    before any write. Stop and report what's wrong rather than silently
    adapting to a changed schema."""
    data = _request("GET", f"https://api.notion.com/v1/databases/{_db_id()}")
    actual = set(data["properties"].keys())
    missing = EXPECTED_PROPERTIES - actual
    if missing:
        raise NotionError(
            f"Database is missing expected properties: {sorted(missing)}. "
            "Stop and fix the database. Do not improvise a workaround."
        )


def query_all(filter_=None):
    """Return every page in the database (paginated), optionally filtered
    with a Notion API filter object."""
    pages, cursor = [], None
    while True:
        body = {"page_size": 100}
        if filter_:
            body["filter"] = filter_
        if cursor:
            body["start_cursor"] = cursor
        data = _request("POST", f"https://api.notion.com/v1/databases/{_db_id()}/query", body)
        pages.extend(data["results"])
        if not data.get("has_more"):
            return pages
        cursor = data["next_cursor"]


def find_by_company(company_substring):
    """Case-insensitive substring match on Company (title). Returns the raw
    page objects , narrow by role and resolve ambiguity in the skill logic,
    never here."""
    return query_all({
        "property": "Company",
        "title": {"contains": company_substring},
    })


def get_text(page, prop):
    """Read a rich_text or title property back out as a plain string."""
    val = page["properties"].get(prop, {})
    parts = val.get("rich_text") or val.get("title") or []
    return "".join(p["plain_text"] for p in parts)


def get_select(page, prop):
    val = page["properties"].get(prop, {}).get("select")
    return val["name"] if val else ""


def get_date(page, prop):
    val = page["properties"].get(prop, {}).get("date")
    return val["start"] if val else ""


def has_job_description(page_id):
    """True if the page body already has a 'Job Description' toggle block."""
    data = _request("GET", f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100")
    for block in data["results"]:
        if block["type"] == "toggle":
            text = "".join(t["plain_text"] for t in block["toggle"]["rich_text"])
            if text == "Job Description":
                return True
    return False


def count_pages():
    return len(query_all())


def create_page(properties, children=None):
    payload = {"parent": {"database_id": _db_id()}, "properties": properties}
    if children:
        payload["children"] = children
    return _request("POST", "https://api.notion.com/v1/pages", payload)


def update_properties(page_id, properties):
    return _request("PATCH", f"https://api.notion.com/v1/pages/{page_id}", {"properties": properties})


def append_note(page_id, page, new_line):
    """Read-modify-write the Notes property: fetch current text, append a
    newline-separated entry, write back in one PATCH. Never overwrite
    earlier entries."""
    current = get_text(page, "Notes")
    updated = f"{current}\n{new_line}" if current else new_line
    return update_properties(page_id, {"Notes": {"rich_text": [{"text": {"content": updated}}]}})


# --- Property builders for constructing a properties payload ---

def title(value):
    return {"title": [{"text": {"content": value}}]} if value else {"title": []}


def rich_text(value):
    return {"rich_text": [{"text": {"content": value}}]} if value else {"rich_text": []}


def select(value):
    return {"select": {"name": value}} if value else {"select": None}


def date(value):
    return {"date": {"start": value}} if value else {"date": None}


def url(value):
    return {"url": value} if value else {"url": None}


def number(value):
    return {"number": value} if value not in (None, "") else {"number": None}


def checkbox(value):
    return {"checkbox": bool(value)}
