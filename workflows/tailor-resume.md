# Workflow: the application loop

The sequence you run for every role you take seriously. Most of the skills in this package are steps in it.

```
JD in hand
   |
   v
1. capture-jd          save the posting before anything else
   |
   v
2. recruiter-screen    Phase 1 verdict. Pass = stop.
   |  (go)
   v
3. Phase 2 brief       what to keep, cut, swap, reframe
   |
   v
4. tailor resume       from the master, following the brief
   |
   v
5. cover letter        if the role warrants one (workflows/cover-letter.md)
   |
   v
6. cleanup-pass        on every human-facing piece
   |
   v
7. you sign off        never before
   |
   v
8. resume-pdf          render + verify
   |
   v
9. you send it
   |
   v
10. log-application    only after you confirm it went out
```

## Why the order matters

**Capture before drafting.** A draft is the thing most likely to end a conversation. An uncaptured posting dies there.

**Screen before tailoring.** Tailoring is ten-plus minutes, a PDF, and usually a letter. Most applications vanish. A three-minute screen protects the hour.

**Tailoring isn't applying.** Log only when you confirm it went out. An application that's tailored but unsent, logged as sent, poisons every number you later compute.

**Speed to send is the default.** Most applications vanish into a black hole. A fast, good-enough draft beats six revision rounds. Get to usable, send, move on. The exception is anything you'll reuse: tooling, templates, the master resume, story blocks. Go slow there and test before you call them done.

## Each step, in one paragraph

**1. capture-jd.** Paste the posting into your AI assistant with the capture-jd prompt. Save the file it hands you into `jds/`.

**2 and 3. recruiter-screen.** Run it against the captured JD and your master resume. Read Phase 1. If it says Pass, believe it unless you have a reason not to. If go, add any corrections, say continue, and get the Phase 2 brief.

**4. Tailor.** Copy the master resume, then follow the brief. Use the tailoring prompt in `templates/master-resume-template.md`. Delete and swap. Don't rewrite. Every claim in the tailored version must exist in the master. Any big reframe is a conversation first, not a default.

**5. Cover letter.** Only if the application takes one or the role warrants it. See `workflows/cover-letter.md`.

**6. cleanup-pass.** On every resume, letter, and message. Automatic. No announcement.

**7. Sign off.** Read it once out loud. Check names, dates, numbers, and the company's name spelled exactly as they spell it.

**8. resume-pdf.** Render, verify, and only then send.

**9. Send.**

**10. log-application.** Ask yourself the question the Claude Code version asked out loud after every deliverable: did it go out? If yes, log it. If you don't answer, the tracker doesn't know, and the application is invisible to every follow-up you'd later run.

## Level-specific notes

- Roles above your current level: flag every place your materials read as your current level instead of the target one. Leadership language, scope, and who you influenced.
- Roles at your level: lead with craft and measurable impact.
