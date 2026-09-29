# Workflow: the setup path

The order to build things in. Foundation first, then tools, then the weekly rhythm. Time estimates are suggestions, not measurements. The story blocks and voice profile take longer than people expect.

**A note on order:** the sequence in the Claude Code version was project setup and About Me, then a resume revision, then the story block library built against the revised resume. This path builds blocks first and revises the resume against them. Either works. What matters is that the resume and the blocks end up agreeing. Story blocks are one-time work that pays back forever, so block out a real hour for them.

## Stage 1: the container (about 45 minutes)

1. Set up your assistant: a ChatGPT Project (`chatgpt-setup.md`), a Claude Code working folder (`claude-code-setup.md`), or a Gemini Gem (`gemini-setup.md`). Paste the instructions block from that doc.
2. Upload your current resume.
3. Write **About Me** (`templates/about-me-template.md`). Use the interview prompt if writing about yourself is hard.
4. Run the sanity check at the bottom of that template. If the positioning statement sounds generic, your About Me needs more specifics.

**Done when:** a fresh chat in your project gives you a positioning statement that sounds like you.

## Stage 2: the evidence (half a day)

5. Gather source material and build your **story blocks** (`templates/story-blocks-build-guide.md`). Do the interrogation and overclaim passes. Skipping them is the most common mistake.
6. Revise your resume against the blocks. Every claim on it should trace to a block.

**Done when:** every number on your resume traces to a source, and you have a flagged list of things you still need to confirm.

## Stage 3: the voice (2 to 3 hours)

7. Collect samples and build your **voice profile** (`templates/voice-profile-guide.md`). If you can run Python, run `voice_metrics.py` first.
8. Set up **writing rules** and **craft rules** (`templates/writing-rules-template.md`). Edit hard.
9. Test the cleanup pass (`skills/cleanup-pass.md`) on a paragraph of your own writing and see whether the result still sounds like you.

**Done when:** a 120-word note written from the profile reads like something you'd send.

## Stage 4: the strategy (1 to 2 hours)

10. Write the **search strategy** (`templates/search-strategy-template.md`): diagnosis, targets, positioning, constraints.
11. Build the **target-company list** (`templates/target-companies-template.md`).
12. Optional: assessments (`templates/assessments-guide.md`) if you're stuck on what you want.

**Done when:** you can say your lead positioning claim in one sentence and name your top ten companies.

## Stage 5: the tracker (30 to 60 minutes)

13. Choose Sheets (`tools/tracker-sheets/`) or Notion (`tools/tracker-notion/`) and set it up.
14. Backfill applications you've already sent. Use the backfill rules in `skills/log-application.md`: real Date Applied, one dated Notes line per event.

**Done when:** every application you've already sent is a row, with Channel filled in.

## Stage 6: the tools (an evening)

15. Export your LinkedIn connections. Triage them (`tools/warm-connections-triage/`). About an hour.
16. Open the ATS search console (`tools/ats-search-console/`) and run one pass.
17. Master resume: convert your resume into the tagged master (`templates/master-resume-template.md`).
18. If you use markdown resumes: install what `skills/resume-pdf.md` needs and render a test.

**Done when:** you've run every tool once on real data.

## Stage 7: switch on the weekly cadence

19. Start `workflows/weekly-cadence.md`. If you can only do two days, do Monday and Wednesday.

## After that: keep it alive

- Run `skills/capture-lessons.md` at the end of sessions where you corrected things.
- Update `story-blocks` when something significant changes. Version them.
- Review `target-companies` monthly, ideally on a Friday.
- Run the "reading a rejection or ghosting pattern" prompt once you have 10 or more applications.

## Optional, advanced

`tools/local-models/`. Read its README first and decide whether you need it. Most people don't.
