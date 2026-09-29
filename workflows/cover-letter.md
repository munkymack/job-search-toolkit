# Workflow: cover letters

Short, specific, built from their problem.

## The rules

- **Length:** 200 words or fewer, one screen. About 300 words in three paragraphs when the role warrants it. Never more than three paragraphs.
- **Structure:** lead with **their problem**, then how you solve it. Not your background. Not your enthusiasm.
- **Tone:** a story, not a stat dump. Numbers support the story. They don't drive it.
- **Never mention being between jobs.** Not their business.
- **Sources:** one positioning block plus two specific blocks from your story library. Nothing that isn't a block. Don't invent accomplishments.
- **Banned lines:** "Excited to apply." "Passionate [role] with X years." "Came across your posting." "I believe I'd be a great fit." "Thank you for considering."
- **Don't parrot the JD's language.** Facts show the match.
- **Sign-off:** your first name only, if a sign-off is called for.

## The sequence

1. **Get the JD first. Always.** No JD, no letter. Run capture-jd.
2. **Research first, then share what you found, then draft.** Light touch: what the company does, one or two recent signals (dated), what the team seems to be. Don't go deep unless you're asked or it's a stretch role. Show your findings before you write so you can correct a wrong read.
3. **Find the real ask.** Use the "decode" prompt in `prompts-library.md`, or the recruiter-screen output. The letter answers the real ask, not the bullet list.
4. **Draft.**
5. **Revise, once.** Ask two sharpening questions, no more. Every revision comes with a one-to-two line note on what changed and why.
6. **Cleanup pass.** Automatic.

## Paste-ready prompt

```
Draft a cover letter for the role below. Use only my story blocks, master resume, and About Me for claims. Never invent an accomplishment.

STEP 1: Before drafting, tell me in 5 lines or fewer: what the company does, one or two recent dated signals (search the web; if nothing current turns up, say so; do not fill from memory), and the real ask behind the JD. Wait for my go-ahead.

STEP 2: Draft, following these rules:
- 200 words or fewer (or 3 paragraphs and about 300 if I say the role warrants it).
- Open with their problem. Then how I solve it. Then one specific story that proves it.
- Story, not stat dump. Numbers support.
- Do not mention being between jobs.
- Do not use: "Excited to apply," "passionate," "came across your posting," "I believe I'd be a great fit," "thank you for considering."
- Do not echo the JD's phrasing. Let facts show the match.
- Sign as [first name].

STEP 3: After the draft, ask me one or two sharpening questions. Not five. If I ask for a revision, give me a one-to-two-line note on what changed and why.

STEP 4: Run the cleanup-pass on it. Don't mention that you did.

Put the letter in one fenced code block so I can copy it as plain text.

JOB DESCRIPTION:
[paste]
```

## When you're asked for options

For headlines, angles, or opening lines: give one clear winner and two real alternates. Not three flavors of the same idea.

## After it's written

Ask whether it went out. Offer to log it with log-application. If there's no answer, ask once more, then drop it.

## Common failure modes

- Opens with who you are instead of what they need.
- Restates the resume.
- Three stats and no story.
- A closing paragraph that explains why the letter works.
- A claim in the letter that the resume doesn't support, or the reverse. Resume and letter must agree on what you did.
