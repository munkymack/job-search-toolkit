# Master resume: template and tailoring system

Instead of keeping one resume and editing it for every job, keep one **master** file that contains everything, tagged, and cut it down per role. Tailoring becomes deletion plus a few swaps, targeted at ten minutes.

## Why it works

- Your best material is all in one place, so you don't forget the good bullet.
- The tags remember decisions you already made about which bullet serves which kind of role, so you don't re-decide them every time.
- The "red flags already stripped" list means your preferences about what not to show survive across applications.
- Light touch: match the JD, cut, reword, keep structure. Big reframes are a conversation, not a default.

## The tags (HTML comments, invisible when rendered)

| Tag | Meaning |
|---|---|
| `USE:` | Role types this bullet serves. Delete the bullet if the role type you're tailoring for isn't listed. |
| `CUT-IF:` | Delete this bullet for these role types even if USE lists them. |
| `ALT-x:` | Alternate wording for angle *x*. Swap it in for the default line above it. |
| `KW:` | ATS keywords this bullet covers. For checking coverage against the JD. Never goes on the resume. |

## Role types

Define 4 to 7 for yourself. They're the axes your jobs vary on. A product manager might use `growth-pm, platform-pm, technical-pm, 0-to-1`. An analyst might use `product-analytics, marketing-analytics, finance, data-engineering-adjacent`. A writer might use `senior-ic, lead, content-strategy, brand, performance`.

Each role type gets:
- An alternate summary paragraph
- A skills-keyword cluster at the bottom of the file
- Bullets tagged for it

## The XYZ bullet format

"Accomplished [X], as measured by [Y], by doing [Z]." Numbers first when you have real ones. Use every real number you have. Never invent one, and never round in your favor. Bullet examples:

```
- Cut onboarding time-to-first-value from 21 days to 9 by rebuilding the six-email sequence and in-app checklist around the three actions that predicted retention.
<!-- USE: growth, lifecycle, product-marketing -->
<!-- ALT-lead: Led a three-person team through an onboarding rebuild that cut time-to-first-value from 21 days to 9. -->
<!-- KW: lifecycle, activation, onboarding, email, retention, cross-functional -->
```

## The file skeleton

```markdown
<!-- ============================================================
     MASTER RESUME | TAILORING TEMPLATE
     Source of truth. Do not render this file directly.

     HOW TO TAILOR (target: 10 minutes)
     1. Copy this file to: resume/tailored/markdown/Your Name - Company - Role.md
     2. Read the JD. Decide the role type (list below).
     3. SUMMARY: keep the one matching the role type, delete the rest.
     4. BULLETS: keep 4 to 6 per role, most relevant first. Delete any bullet
        whose USE line does not include your role type, and any with a matching
        CUT-IF. If an ALT- line matches your angle, swap it in.
     5. SKILLS: keep the core line, then paste in the keyword cluster(s) for
        your role type from the SKILLS KEYWORD BANK at the bottom.
     6. Delete every HTML comment (including this block) and the KEYWORD BANK.
     7. Check that it lands on one page. Two pages absolute maximum.
     8. Sign off, then run the PDF step (skills/resume-pdf.md).

     ROLE TYPES: [your list]

     RED FLAGS ALREADY STRIPPED (keep them stripped):
     - [your list; see below]
     ============================================================ -->

# Your Name

City, ST  
(555) 555-5555 | [you@example.com](mailto:you@example.com) | [LinkedIn](https://www.linkedin.com/in/you/) | [Portfolio](https://example.com)

## Summary

<!-- DEFAULT: [role types] -->
[Two sentences about who you are. Not a JD remix.]

<!-- ALT SUMMARY: [role type]. Delete the default above, uncomment this.
[alternate summary]
-->

## Experience

**Employer** *(formerly Old Name)*  
**Title** | 20XX to 20XX

- [XYZ bullet]
<!-- USE: ... -->
<!-- ALT-x: ... -->
<!-- KW: ... -->

## Skills

**Core:** [always-on line]  
**Tools:** [always-on line]

## Education

## SKILLS KEYWORD BANK (delete before rendering)
<!-- CLUSTER role-type-1: keyword, keyword, keyword -->
<!-- CLUSTER role-type-2: ... -->
```

## "Red flags already stripped": decide your own list

The most useful section of this template. It records decisions about what the resume shouldn't volunteer. Examples, to give you the idea:

- No year count in the summary. "15 years" invites "overqualified."
- Years only, no months, anywhere. Hides small gaps.
- Title of record vs. resume title. If your official title differs from what the work was, use the accurate short version on the resume and the full title only on application forms and background checks.
- Older or off-target jobs carry no dates, or are cut, and get pulled back only if a JD makes them relevant.
- Formatting rule, not a red flag: no em dashes.

Be honest with yourself here. Hiding a gap on a resume is your call, but never misstate a title, date, or claim. The list is for what to *omit*, not what to falsify. Anything you'd be uncomfortable explaining in an interview doesn't belong on the page.

## The line-break gotcha (matters if you render to PDF)

Where two lines are meant to be separate (location above phone, employer above title-and-dates, two bold label lines in Skills), the first line must end with **two trailing spaces**. Otherwise markdown runs them into one paragraph. Editors love to trim trailing whitespace, so turn that off for this file. See `skills/resume-pdf.md`.

## Filename convention

`Your Name - Company - Role.md`, using the company's own capitalization and dropping commas. Save PDFs with the same base name.

## Working with the AI on it

1. Upload the master to your project.
2. Run recruiter-screen first. Its Phase 2 brief tells you which bullets to keep, cut, swap, and what to reframe.
3. Have the AI produce the tailored version by *following the brief*, deleting and swapping only. Then check every line against the master. Anything in the tailored version that isn't in the master needs a source.
4. Run the cleanup pass on the result (`skills/cleanup-pass.md`).
5. Sign off. Render.

Prompt for step 3:

```
Tailor my master resume to this role using the recruiter-screen brief above. Follow the master's own instructions: keep the matching summary, delete non-matching bullets by their USE and CUT-IF tags, apply ALT lines where the brief says to, add the matching keyword cluster to Skills, and delete all HTML comments.

Do not add any claim that isn't in the master. Do not change any number. Do not reframe beyond what the brief specified. If the brief asks for something the master can't support, tell me instead of inventing it.

Keep the two-trailing-space line breaks in the header and wherever bold lines sit back to back.

Output the resume in one fenced code block, then two lines on what changed and why.
```
