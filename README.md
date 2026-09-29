# Job search toolkit

A working job search system: skills, workflows, tools, and templates, packaged to run in ChatGPT, Claude Code, or Gemini.

**Start with `overview.md`.** It walks every step, tool, and skill in order. Then the setup doc for your assistant (`chatgpt-setup.md`, `claude-code-setup.md`, or `gemini-setup.md`), then `workflows/setup-path.md`.

## What's in the folder

```
README.md               this file
overview.md             every step, tool, and skill
chatgpt-setup.md        setup for ChatGPT: instructions block, file list, what it can't do
claude-code-setup.md    setup for Claude Code: CLAUDE.md, working folder, optional skills
gemini-setup.md         setup for Gemini: Gem instructions, knowledge files, what it can't do

skills/                 8 paste-ready procedures (capture-jd, recruiter-screen,
                        log-application, pipeline-sweep, draft-followup,
                        cleanup-pass, resume-pdf, capture-lessons)

workflows/              multi-step procedures
  setup-path.md         the order to build things in
  tailor-resume.md      the 10-step application loop
  cover-letter.md
  linkedin-outreach.md
  warm-network-mining.md
  weekly-cadence.md
  prompts-library.md

templates/              documents you fill with your own material
  about-me-template.md
  story-blocks-build-guide.md
  voice-profile-guide.md
  writing-rules-template.md   (writing rules + craft rules)
  search-strategy-template.md
  target-companies-template.md
  master-resume-template.md
  portfolio-context-template.md
  assessments-guide.md
  outreach-templates.md

tools/                  things you run on your own machine
  warm-connections-triage/    LinkedIn export -> Warm/Skip -> JSON
  ats-search-console/         Google searches scoped to each ATS
  resume-pdf/                 PDF verifier (Python + poppler)
  tracker-sheets/             Google Sheets / Excel tracker schema
  tracker-notion/             Notion tracker + Python client
  local-models/               voice metrics and optional local extraction
```

## The fastest useful path

If you only have an hour: set up your assistant (see your setup doc), write About Me (`templates/about-me-template.md`), then build your story blocks (`templates/story-blocks-build-guide.md`). Everything else is better once those exist.

## Privacy

Nothing in this package contains anyone's personal data: no connections, contact details, applications, or API keys. Read the privacy notes in your setup doc and `tools/warm-connections-triage/README.md` before uploading your connection list.

## License

MIT. See `LICENSE`.

## Credits

The cleanup-pass draws on the open-source humanizer skill (MIT, based on Wikipedia's "Signs of AI writing") and Hardik Pandya's stop-slop (MIT).
