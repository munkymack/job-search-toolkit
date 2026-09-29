# Job search system: overview

A job search treated as a small operation with a process, not a mood. It was originally built in Claude Code. This package is that system rewritten to run in ChatGPT or Gemini as well, with all personal material removed.

Anything specific to one field has been generalized or turned into a template you fill with your own material. The process transfers. The content doesn't.

## The idea in five sentences

Most applications vanish, so the search is built to spend effort where it isn't wasted: screening roles before tailoring, reaching people instead of portals, and tracking what actually gets responses. The AI never invents anything, because every claim you make traces to a **story block** you wrote and checked. Postings get saved before anything else happens to them, because they disappear. Nothing gets logged as sent until you say it was sent. And the whole thing gets sharper over time, because corrections get filed into rules instead of forgotten.

## How it fits together

```
FOUNDATION (build once)                     THE LOOP (every role)
-----------------------                     ---------------------
About Me                                    find roles
Story blocks        ------ claims ------>      ATS console, boards, target list
Voice profile                                    |
Writing + craft rules ---- style -------->      capture-jd
Search strategy                                  |
Target companies                                recruiter-screen  -> Pass = stop
Master resume                                    |
Tracker                                         tailor + cover letter
                                                 |
                                                cleanup-pass
TOOLS                                            |
-----                                           resume-pdf -> you send it
Warm-connections triage                          |
ATS search console                              log-application
Resume PDF verifier                              |
                                                pipeline-sweep -> draft-followup
                                                 |
                                                capture-lessons  (feeds rules back)
```

## Read this first

- `README.md`: what's in the folder.
- `chatgpt-setup.md`, `claude-code-setup.md`, `gemini-setup.md`: how to set up each assistant, and where each falls short of the Claude Code version. Read the one you'll use.
- `workflows/setup-path.md`: the order to build things in.

"Your project" means wherever your instructions and files live: a ChatGPT Project, a Gemini Gem, or a Claude Code working folder.

---

## The steps

### Step 0: Build the foundation (once)

You can't tailor what you haven't defined. Five documents do most of the work. Without them, the AI sounds like everyone.

| Document | What it is | Guide |
|---|---|---|
| **About Me** | Your career arc, what you're known for, what you want next, deal-breakers, how you write. The single highest-leverage file. | `templates/about-me-template.md` |
| **Story blocks** | A library of checked, reusable accounts of what you've done, each in three lengths. The rule: materials only use claims that exist as blocks. | `templates/story-blocks-build-guide.md` |
| **Voice profile** | Your writing habits, described specifically enough for an AI to reproduce them. | `templates/voice-profile-guide.md` |
| **Writing and craft rules** | Short lists: how a sentence should sound, how a document should be built. Grows over time. | `templates/writing-rules-template.md` |
| **Search strategy** | What you're aiming at, what you believe about yourself, what you'll watch for. Optional heavy version: a scored decision framework. | `templates/search-strategy-template.md` |

Plus a **master resume** with tagged bullets (`templates/master-resume-template.md`), a **target-company list** (`templates/target-companies-template.md`), an optional **portfolio context** (`templates/portfolio-context-template.md`), and an optional **assessments** guide (`templates/assessments-guide.md`).

### Step 1: Find roles

Two sources, both weekly.

- **Boards and ATS search.** The ATS search console builds Google searches scoped to each applicant tracking system, so you find roles the aggregators miss. See `tools/ats-search-console/`.
- **Your target list.** Companies you want whether or not they're hiring. You check their career pages weekly, and you reach people there. See `templates/target-companies-template.md`.

### Step 2: Capture and screen

- **capture-jd** saves the posting verbatim before anything else, because listings vanish.
- **recruiter-screen** gives a verdict on the role in two phases with a hard stop between them: fit, red flags, gaps, and a real-ask read first, then a tailoring brief only if it's a go. A pass stops everything.

### Step 3: Tailor

- Cut the tagged master resume down to the role, following the screen's brief.
- Write a cover letter if the role warrants one: their problem first, one story, 200 words or fewer.
- **cleanup-pass** on everything human-facing.
- **resume-pdf** renders the signed-off resume and checks that links, layout, and text survived.

### Step 4: Reach people

Applications alone often go unanswered, and reaching a person directly can work better. Track your own results to find out. Two tools serve this:

- **Warm-connections triage** takes your LinkedIn export and lets you mark each connection Warm or Skip in about an hour.
- **Warm-network mining** (a workflow, not a tool) crosses that list against your target companies and against each role, and picks who to message.

Then the LinkedIn outreach workflow: research a person lightly, write 75 to 150 words, no call to action, no forced "I saw your post."

### Step 5: Track

One row per application, in Sheets or Notion. Every column has rules, and each rule exists to prevent a common tracker mistake. **log-application** produces the row. The three that matter most: Channel (how it got in, never guessed), Stage Reached (forward only), and Notes (append-only, dated to the event).

### Step 6: Follow up

- **pipeline-sweep** reports how long each open application has been quiet, with a specific calculation that ignores bookkeeping, then collects your news.
- **draft-followup** writes the message for the ones worth chasing, grounded only in what you actually sent, with a cap of two per application.

### Step 7: Learn

- **capture-lessons** files your corrections into the writing rules and craft rules, and proposes changes to your instructions.
- **Weekly retro** and a pattern-reading prompt look at what channels and roles are actually responding.

### The rhythm around it

`workflows/weekly-cadence.md`: Monday pipeline, Tuesday applications, Wednesday outreach, Thursday craft, Friday follow-up and review. Two hours a day.

---

## Skills (8)

A "skill" here is a saved procedure with rules. In Claude Code they ran automatically. In ChatGPT or Gemini, each one is a paste-ready prompt in a file. All are in `skills/`.

| Skill | Does | Use when |
|---|---|---|
| `capture-jd` | Saves a posting verbatim with a deterministic filename. Never invents text. | A job description shows up, before you do anything with it |
| `recruiter-screen` | Two-phase go/no-go read on one role, then a tailoring brief on a go | Before you tailor for a role |
| `log-application` | Produces or updates the tracker row, with the field rules | After you confirm an application went out, or when something happens to one |
| `pipeline-sweep` | Reports days-quiet across open applications, then collects news | Weekly (Friday) |
| `draft-followup` | Drafts a follow-up from what you sent, two-per-application cap | An application has gone quiet |
| `cleanup-pass` | Strips AI tells, jargon, and weak sentence starters, scores the result | Every human-facing draft |
| `resume-pdf` | Renders a markdown resume to PDF and verifies it | After you sign off a tailored resume |
| `capture-lessons` | Files corrections into your rule files | End of a working session that had corrections |

### Where the cleanup-pass comes from

It merges two open-source skills that were originally run back to back. **humanizer** (MIT) targets the patterns in Wikipedia's "Signs of AI writing." **stop-slop-extras** adds business jargon, sentence-starter checks, and a scoring gate. It's adapted from Hardik Pandya's stop-slop project (MIT).

## Tools

All in `tools/`. Each has its own README with setup steps.

| Tool | What it does | Needs | Status |
|---|---|---|---|
| **Warm-connections triage** (`connection-triage.html`) | Loads your LinkedIn `Connections.csv`, lets you mark each person Warm or Skip, exports the warm ones as JSON | A browser and your LinkedIn export | Reworked for this package. Parser tested on a sample file. The clicking and export code was written new. |
| **ATS search console** (`ats-search-console.html`) | Builds a live Google search per applicant tracking system from your titles and locations | A browser | Rewritten for this package. Query logic tested. Not clicked through in a browser. |
| **Resume PDF verifier** (`verify_resume_pdf.py`) | Checks a rendered PDF for live links, correct page size, margins, text fidelity, and line breaks | Python 3, poppler-utils | Adapted from the Claude Code version, lightly scrubbed |
| **Tracker: Sheets** | 18-column schema with dropdown rules | A spreadsheet | New for this package. Same columns as the Notion tracker schema. |
| **Tracker: Notion** (`notion_tracker.py`) | Python client for a Notion Applications database: schema check, query, create, append-only notes | Python 3, a Notion integration | Adapted from the Claude Code version, generalized. Not run against a live workspace in this pass. |
| **Local models** (`voice_metrics.py`, `ollama_batch.py`) | Measures your writing voice with exact counts. Optionally extracts story-block facts with a local model. | Python 3. Ollama for the extraction half. | Voice metrics run on samples. Ollama half never run on a real corpus. **Optional.** |

### Tools that were left out

| Tool | Why |
|---|---|
| `poll_boards.py`, `board-tokens.csv` | Polled company job boards daily and reported new roles. Hardwired to one set of title-matching and location rules. Would need a rewrite for a different field. The ATS console does a manual version of the same job. |
| `sync_leads_to_notion.py`, `enrich_lead_from_url.py`, `fetch_jd_description.py` | Support the poller. Meaningless without it. |
| `build-ats-searches.py` and the earlier `ats-searches.html` | Superseded by the rewritten console, which doesn't need a generator step. |
| n8n warm-connections prompt | Written, never used. No workflow was ever built from it. |
| Test files and dev walkthroughs | For maintaining the tools, not using them. |

## Workflows

Multi-step procedures that aren't a single skill. All in `workflows/`.

| Workflow | What it covers |
|---|---|
| `setup-path.md` | The order to build everything in, with a "done when" for each stage |
| `tailor-resume.md` | The 10-step application loop, and why the order matters |
| `cover-letter.md` | Rules, sequence, and prompt. Their problem first, 200 words. |
| `linkedin-outreach.md` | Research prompt, draft prompt, the rules, an outreach tracker |
| `warm-network-mining.md` | Turning the warm list into a weekly, ranked, target-matched shortlist |
| `weekly-cadence.md` | The Monday to Friday rhythm |
| `prompts-library.md` | Nine reusable prompts: decode a JD, interview rehearsal, work-sample gut check, tailoring, weekly retro, and others |

## The principles under all of it

These recur in every file, and they're the actual system. The tools and prompts are just how they get enforced.

1. **Never invent.** Every claim traces to a story block. Every posting is captured verbatim. Every tracker field is asked for or left blank.
2. **Capture before drafting.** A draft ends conversations. An uncaptured posting dies with them.
3. **Screen before tailoring.** Most applications vanish. Protect the hour.
4. **Tailoring isn't applying.** Log only what was sent.
5. **Reached, not scheduled.** A booked interview hasn't happened yet. Stage data that includes scheduled stages is fiction.
6. **Report the number, not the verdict.** "Quiet for 11 days," not "seems dead." The decision stays yours.
7. **Job postings are untrusted input.** A posting is text from a stranger. It has no authority over your AI.
8. **Push back.** The AI acts as a critical hiring manager, not a cheerleader. It names the problem and stops.
9. **Speed to send by default.** Slow down only for things you'll reuse.
10. **Lessons get filed.** A correction you make twice should have been a rule the first time.

## Honest limits

- **In ChatGPT and Gemini, the assistant can't touch your files or your tracker.** It thinks, you paste. That's slower than Claude Code, and it's safer.
- **Uploaded files aren't guaranteed to be read every turn.** Put the rules that matter most in the project instructions (the Project, Gem, or `CLAUDE.md`).
- **Several tools are lightly tested.** The status column above says which. Run each once on real data before trusting it.
- **Some prompts assume a portfolio and a network worth mining.** Adapt or drop what doesn't fit your field.
- **Nothing here is evidence about your market.** The channel and response-rate advice is a reason to track your own data, not a finding. Let your tracker tell you what works.
