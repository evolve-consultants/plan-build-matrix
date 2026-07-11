**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
Users find an existing dashboard confusing, and you want it fixed. But I don't have the dashboard itself, the actual complaints, or any data about what's going wrong — so "fix it" currently has no concrete target.

<assumptions>
  <project>Unknown: I don't know what this dashboard shows, what tech stack it's built on, who owns it, or whether it's internal tooling vs. customer-facing.</project>
  <task>Unknown: I don't know if "confusing" means information overload, poor layout, unclear labels, bad information architecture, performance/loading confusion, or something else entirely.</task>
  <operator>Unknown: I don't know if you want a full redesign, a quick patch, a research phase first, or if you already have specific complaints in hand that you haven't shared yet.</operator>
</assumptions>

### What I'm unsure of
- What the actual user complaints say — verbatim quotes, support tickets, or survey data would tell us a lot
- Which users are complaining (new users? power users? a specific segment?) — "confusing" means different things to each
- Whether this is a visual/UX problem, an information architecture problem, or a data/content problem
- Whether you have analytics (drop-off points, click patterns, session recordings) that show *where* people get stuck
- Whether I can see the dashboard (screenshot, code, live link) at all

### Options
| | Upside | Downside | Best when |
|---|---|---|---|
| **A: Diagnose first** — gather actual complaint text, analytics, and a look at the dashboard before proposing changes | Fixes the real problem, not a guessed one | Slower to a visible output | You have complaint data or analytics available |
| **B: Heuristic review** — I review a screenshot/description against standard UX/dashboard-design heuristics (visual hierarchy, cognitive load, progressive disclosure) and propose fixes | Fast, gets a concrete artifact quickly | Risk of solving a problem users don't actually have | You just need a sanity-check pass and don't have hard data |
| **C: You share raw complaints, I categorize them** — paste in ticket/survey text, I cluster it into themes (e.g., "can't find X", "too much data at once") | Grounds the fix in real user language | Doesn't produce design changes yet, just diagnosis | You have qualitative feedback but haven't organized it |

### Recommendation
Option A, starting with C as its first step — pull the actual complaint text (even a handful of representative quotes) and, if possible, a screenshot or description of the dashboard. Guessing at a fix for "confusing" without seeing either the complaints or the interface risks solving the wrong problem entirely.

### Next prompt should include
- A few real user complaints (verbatim, if possible) or a link/description of where these complaints come from
- A screenshot, mockup, or description of the current dashboard
- Who the users are (role, technical familiarity, how often they use it)
- Any constraints: tech stack, timeline, whether this is a redesign or incremental fix