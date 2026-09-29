# Skill: resume-pdf

Renders a signed-off markdown resume into a matching PDF, then checks the PDF isn't broken.

## Why this exists

Two failure modes are easy to miss: header links (LinkedIn, portfolio) that rendered as plain text instead of real hyperlinks, and PDFs where the location and phone number collapsed onto one line. Both look fine on screen and wrong to the person reading. The verify step catches them.

## Is this worth it for you?

Only if your resume lives in markdown. If you keep it in Google Docs or Word, skip this: export to PDF from there and use your own eyes, and use the link checklist at the bottom. The markdown route buys you a clean text source that an AI can tailor without mangling formatting, and files you can version.

## Requirements

- Node.js, so `npx` works (installs `md-to-pdf` on first run)
- `poppler-utils` for the verify script (`pdftotext`, `pdfinfo`, `pdftohtml`). On Mac: `brew install poppler`. On Ubuntu or Fedora: install the `poppler-utils` package.
- Python 3 for the verify script. No pip installs.

## When to run it

After you sign off on a tailored resume. Not on every edit. PDFs shouldn't regenerate mid-revision.

## Folder and naming convention

```
resume/tailored/markdown/Your Name - Company - Role.md
resume/tailored/pdf/Your Name - Company - Role.pdf
```

Same base name in both folders, different extension. That's what keeps this mechanical instead of needing a lookup table. Use the company's own capitalization (HAUS, JPMC, not Haus, Jpmc). Drop commas from filenames ("Brand Voice Lead, Systems" becomes "Brand Voice Lead Systems" in the filename only). Never invent a company or role name to force a filename to fit. Ask.

## Render

From the folder that holds `resume/`:

```bash
npx --yes md-to-pdf --document-title "Your Name - Company - Role" \
  --pdf-options '{"format":"Letter","margin":{"top":"18mm","right":"16mm","bottom":"18mm","left":"16mm"}}' \
  "resume/tailored/markdown/Your Name - Company - Role.md"

mv "resume/tailored/markdown/Your Name - Company - Role.pdf" "resume/tailored/pdf/Your Name - Company - Role.pdf"
```

Three details, each learned from a bug:

- **`--document-title`**: without it, the PDF's Title metadata is a localhost URL, which shows up in browser tabs and file properties.
- **`"format":"Letter"`**: md-to-pdf defaults to A4 silently. If you're applying in the US, you want Letter. Use `A4` if you're not.
- **The `margin` block is required.** `--pdf-options` replaces the tool's whole default options object, including its default margin. Pass only `format` and the text runs edge to edge. This shipped broken once.

## The two-space line break

In markdown, two lines with no blank line between them merge into one paragraph. md-to-pdf will run them together. Every place you want a forced break needs two trailing spaces at the end of the line:

- The location line above the phone line in the header
- The employer line above the title-and-dates line in every Experience entry
- Any pair of bold label lines in Skills, like "Strategy & Research:" above "Tools:"

Editors trim trailing whitespace. Turn that off for this file, or the break disappears silently.

## Verify

```bash
python3 tools/resume-pdf/verify_resume_pdf.py "resume/tailored/markdown/<name>.md" "resume/tailored/pdf/<name>.pdf"
```

It derives every expectation from your markdown, not from hardcoded contact info. It checks that the PDF has extractable text, that every link in the markdown survived as a real clickable annotation (not just visible text), that the title is set, that the page size is Letter, that the margins aren't zero, that text extraction fidelity is high enough to rule out garbling, and that bold line pairs have their hard breaks. A non-zero exit means at least one FAIL. A WARN (for instance, more than two pages) doesn't block.

On a FAIL: stop. Don't send the PDF. Fix the cause and re-render.

## Rules to keep

1. Only run after sign-off.
2. Same base filename in both folders.
3. Never send a PDF that hasn't passed verify.
4. Default styling only. Custom print CSS is a separate project. Don't start it mid-search.
5. LinkedIn and Portfolio in the header must be real hyperlinks, not placeholder text.

## If you skip the markdown route: manual checklist

- Click every link in the exported PDF
- Location and phone on separate lines
- Text is selectable (not an image)
- Two pages at most
- The PDF's file name is the one you meant to send
