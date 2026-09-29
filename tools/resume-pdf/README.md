# Tool: verify_resume_pdf.py

Checks that a rendered resume or cover letter PDF isn't quietly broken.

Full workflow, including the render command and the naming convention, is in `skills/resume-pdf.md`. This file is only about the script.

## What it checks

Every expectation is derived from your markdown source. Nothing is hardcoded, so it works for resumes and cover letters with no mode flag.

| Check | Severity | What it catches |
|---|---|---|
| Extractable text | FAIL | A PDF that's really an image |
| Every link in the markdown survived as a real clickable PDF annotation | FAIL | LinkedIn or Portfolio rendering as plain text |
| PDF Title metadata is set correctly | FAIL | A localhost URL as the document title |
| Page size is US Letter | FAIL | A4 by default |
| Margins above a minimum | FAIL | Text running edge to edge because the margin option was dropped |
| Text extraction fidelity at or above 90% | FAIL | Garbled or missing text |
| Bold line pairs have their hard breaks | FAIL | Employer and title running together on one line |
| Page count over two | WARN | Resume too long |

Exit code is non-zero on any FAIL. A WARN doesn't change it.

## Run it

```bash
python3 verify_resume_pdf.py "path/to/resume.md" "path/to/resume.pdf"
```

## Requirements

Python 3.9 or newer, and `pdftotext`, `pdfinfo`, and `pdftohtml` from `poppler-utils`. No pip packages. If the tools are missing, the script says which.

- Mac: `brew install poppler`
- Ubuntu / Debian: `sudo apt install poppler-utils`
- Fedora: `sudo dnf install poppler-utils`
- Windows: use WSL, or skip this tool and use the manual checklist in `skills/resume-pdf.md`

## Adjusting it

The constants at the top: `FIDELITY_FLOOR` (0.90), `MAX_PAGES` (2), `MIN_MARGIN_PT` (22 points, about 7.8mm). The Letter-size check is in `check_page_size`. Change it if you're applying with A4.

## Status

Adapted from the Claude Code version, with personal references removed from comments. Otherwise unchanged.
