# Building your story block library

The single highest-payoff piece of prep in the search. It's one-time work that pays back on every application. Block out a real hour. Don't try to do it in 15 minutes.

## What a story block is

A short, reusable, evidence-backed account of one thing you did. You write it once, carefully, then assemble applications from blocks instead of rewriting from scratch each time.

The problem it solves: tailoring feels repetitive because you're rewriting the same accomplishments in slightly different words. The fix is assembling, not rewriting. Pull two or three blocks that match the job, and the tailoring is mostly done.

The second problem it solves: AI invents things. If the AI only writes from a library of claims you've verified, it can't inflate them. The rule for your whole search becomes: **materials only use claims that exist as blocks.**

## The anatomy of a block

Every block has the same fields.

| Field | What goes in it |
|---|---|
| **ID** | A short, stable, kebab-case name like `q3-onboarding-rebuild`. You'll reference it constantly. |
| **One sentence** | For outreach and resume bullets. Contains the number, if there is one. |
| **Three sentences** | For cover letters. Situation, what you did, what happened. |
| **Paragraph** | For interviews. This is your STAR-story scaffolding. |
| **Skills** | What it demonstrates, in the words a hiring manager would use |
| **Best for** | Role types and job descriptions where this block should lead |
| **Level read** | Does it read as individual-contributor strength, leadership, or both? |

## The categories

Group blocks by the job they do in an application. A mature library might have 25 blocks across seven categories. Yours will differ, but start from these and delete what doesn't fit:

1. **Measurable results.** Numbers. Percentages, dollars, volume, time saved. The blocks that get quoted.
2. **Range.** Evidence you can operate across different kinds of work or audiences, without being a dabbler.
3. **Signature or differentiating work.** Things a peer with the same title probably hasn't done. This is what makes you memorable.
4. **Leadership signals.** Building a system others use, running a team, influencing without authority, mentoring, owning a process. Essential if you're aiming at a lead or manager role. Also worth having if you aren't, because it shows up as "senior."
5. **Subject-matter depth.** Where you had to learn a domain fast or write, sell, build, or decide for an expert audience.
6. **Tools and AI in the workflow.** Production proof, not tool-list claims. "Cut turnaround by X by doing Y" beats "proficient in AI tools."
7. **Positioning hypotheses.** Claim-shaped blocks, like "the person who speaks both engineering and marketing." These are reusable framings, backed by two or three of the blocks above. Treat them as hypotheses until interview feedback confirms them.

## The process

### 1. Gather source material

More is better. Anything that shows what you did:

- Your current resume, and older ones
- Past cover letters (even rough ones)
- Performance reviews and self-assessments
- LinkedIn recommendations others wrote about you
- Portfolio pieces or case studies
- Project write-ups, launch announcements, slide decks
- Personality or work-values assessments, if you've taken them (see `assessments-guide.md`)
- Old emails where someone thanked you for something specific

Put it in one folder. Upload it to your project or paste it in chunks.

### 2. Run the extraction prompt

```
I'm building a modular content library to make tailoring job applications faster. Below are my resume, past cover letters, and other source material.

Extract every distinct accomplishment, project, leadership moment, or skill demonstration into a reusable "story block."

For each block:
1. ID: a short kebab-case name.
2. Three versions: one sentence, three sentences, and a full paragraph.
3. Skills it demonstrates.
4. What kind of role or job description it is best deployed for.
5. Level read: does it read as individual contributor, leadership, or both?
6. Category: measurable result, range, signature work, leadership signal, subject-matter depth, tools/AI in the workflow, or positioning hypothesis.

HARD RULES
- Use only what is in the source material. Never invent a number, a team size, a client, or an outcome. If a fact isn't stated, write UNKNOWN in that spot.
- Copy numbers exactly as written. Never round or convert them.
- Never write an adjective that isn't in the source ("successful," "significant," "impactful").
- Keep scope words honest. "Contributed to" is not "led." "Edited some" is not "built the system." "A system" is not "the system."
- If two documents describe the same project differently, list both versions and flag the conflict.

Give me the blocks, then a list of every UNKNOWN and every conflict.

[paste source material]
```

### 3. The interrogation pass

The first draft will have holes, and the holes are where the risk is. Ask the AI to interview you about them.

```
Look at the blocks you just wrote. For each one, list the questions a skeptical hiring manager would ask that the source material doesn't answer. Focus on:
- Team size: did I do this solo, with vendors, or leading other people?
- Ownership: what exactly was mine versus the team's?
- Metrics: is there data I could recover, like dashboards, reports, or an old email?
- Collaborators: who else was involved, and what did I direct versus receive?
- Duration and dates.

Then ask me those questions one block at a time, and wait for my answer. Update each block with what I tell you.
```

This is the step that turns a resume remix into a defensible library. Expect it to take longer than the extraction. A good library ends with a flagged list of unanswered questions ("was the year-long campaign solo with vendor support, or did I lead other people? confirm before using leadership framing"). Keep such a list too. Unresolved questions are fine. Unresolved questions hidden inside confident prose are not.

### 4. The overclaim audit

```
Audit every block for claims that outrun the evidence. For each block, list:
1. Every scope word (owns, led, built, system, every, all, drove) and whether the source supports it.
2. Any claim of expertise or fluency that the work only touched.
3. Any place two adjacent claims imply a causal link the source doesn't establish.
Rewrite anything that fails. When in doubt, use the smaller claim.
```

For example, a block might claim technical fluency in a regulated domain because you've written for that audience, when the work shows range across verticals but not technical depth. Cut the block back to claim range only. That's the audit doing its job.

### 5. Check the numbers against the source

Pick every number in the library and trace it to a document. If you can't, either find the source or delete the number. A number you can't defend in an interview is a liability.

### 6. Write positioning blocks last

Once the evidence blocks exist, ask:

```
Based only on the blocks above, propose 4 positioning hypotheses. Each should be a claim-shaped sentence that a hiring manager would remember, and each must list the 2 to 3 blocks that back it. Flag any hypothesis where the evidence is thin.
```

Pick your lead claim from these, and treat the rest as hypotheses to test against real responses over the first month.

### 7. Version it

Save as `story-blocks-v1.md` with the date. When something significant changes (a new role, interview feedback that shifts your read, a recovered metric), make v2 and keep a short "what changed" note at the bottom. Expect several versions in the first few months. Blocks should change as you learn.

## An example block (fictional)

```
### `onboarding-rebuild`: Customer onboarding rebuild
- **Category:** Measurable result
- **One sentence:** Rebuilt the customer onboarding sequence for a 40-person SaaS company, cutting time-to-first-value from 21 days to 9 and trial-to-paid conversion from 11% to 16%.
- **Three sentences:** When I joined, new customers waited an average of 21 days to reach their first successful use, and only 11% of trials converted. I rewrote the six-email onboarding sequence and rebuilt the in-app checklist around the three actions that predicted retention. Time-to-first-value fell to 9 days and trial-to-paid conversion rose to 16% within two quarters.
- **Paragraph:** [4 to 6 sentences: the situation, how I found which three actions mattered, what I changed, who I worked with, what was hard, and the result.]
- **Skills:** Lifecycle email, activation analysis, cross-functional work with product and support
- **Best for:** Growth, lifecycle, and customer-marketing roles at product-led companies
- **Level read:** Individual contributor. Leadership only if the source shows I directed others.
- **Sources:** Q2 retro deck, review from June
```

## How to use the library

| Situation | What to pull |
|---|---|
| Tailoring an application | 2 or 3 blocks matching the JD's stated and unstated needs. Use the "Decode a job listing" prompt first (`workflows/prompts-library.md`). Build the cover letter from one positioning block plus two specific blocks. |
| Outreach | One-sentence versions only. Positioning blocks are usually too long for a message. |
| Interview prep | Paragraph versions are STAR-story scaffolding. |
| Self-audit | When a JD asks for something, check whether you have a block for it. If not, it's either a real gap (good to know) or evidence your resume undersells something (good to fix). |
| Follow-ups | Nothing new. Follow-ups may only repeat claims already in what you sent. |

## The rules that keep it honest

1. Materials use claims that exist as blocks. If a claim isn't there, ask yourself whether it's true, prove it, add the block, then use it.
2. Match claims to blocks exactly. Don't inflate a partial contribution into full ownership.
3. Resume and cover letter agree on what you did.
4. Match positioning to the role level. Don't surface leadership blocks for a role that wants a hands-on specialist, and don't hide them for a role that wants a lead.
5. Don't claim keywords you can't back.

## The local-model shortcut (optional)

If your source material is large or sensitive, `tools/local-models/` can extract facts into a fixed schema on your own machine first. It never writes the blocks. It only extracts. Skip it unless you have that use case.
