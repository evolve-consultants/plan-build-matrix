**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You have customer records in four different systems with conflicting data, and you need a strategy to resolve the inconsistencies and prevent it from happening again.

<assumptions>
  <project>You have some ability to query/export data from these systems. You probably can't immediately rip-and-replace them. At least one system is likely the source of truth or closest to it.</project>
  <task>You want a practical path to either reconcile the data now, establish a single source of truth going forward, or both.</task>
  <operator>You're looking for framework/strategy rather than implementation details at this stage. You have decision-making authority but probably need to justify choices to stakeholders.</operator>
</assumptions>

### What I'm unsure of
- **Scope of disagreement**: Are we talking about a few fields (address, phone) or entire records? A few customers or thousands?
- **System roles**: Which system(s) are authoritative? Are they all "primary" or is one clearly the source of truth that others sync from?
- **Update frequency**: Are these one-time batch loads, real-time syncs, or manual entry? How often do inconsistencies emerge?
- **Constraints**: Do you need to fix this retroactively, prevent it going forward, or both? What's your timeline?
- **Stakeholder buy-in**: Is this a known problem with agreed-upon urgency, or are you building the case for action?

### Options

| | Upside | Downside | Best when |
|---|---|---|---|
| **A: Audit first, fix selectively** | Low risk. Reveals the true scope before big decisions. Buys time to build consensus. | Doesn't solve the problem quickly. Customers still see inconsistencies. | You need evidence before investing in a fix. Disagreement exists about which system should win. |
| **B: Declare a source of truth + reconcile backward** | Decisive. Establishes clear rules going forward. Fixes the backlog in one move. | High risk if the "winner" is wrong or incomplete. Requires strong governance to prevent re-divergence. | One system is clearly most authoritative and trustworthy. You have stakeholder alignment on the choice. |
| **C: Build a reconciliation layer (middleware)** | Solves immediate pain without touching legacy systems. Can live alongside existing workflows. | Doesn't fix root cause. Adds complexity and ongoing maintenance. False reconciliation hides deeper problems. | Systems can't be touched and customers need a single view immediately. You're buying time before a real fix. |
| **D: Full integration project** | Genuinely fixes the problem. Creates a single source of truth. Prevents future divergence. | Expensive, slow, high risk, requires system downtime or parallel runs. | You have budget, timeline, and organizational will. This is the long-term play. |

### Recommendation
**Start with A (Audit), then move to B (Declare + Reconcile).**

Here's why: You almost certainly don't know the true shape of the problem yet. An audit is cheap insurance — it will tell you whether this is "a few phone numbers are stale" or "entire customer records are duplicated differently across systems." That answer determines everything downstream. Once you have the audit, declaring a source of truth is the fastest path to a stable state that doesn't require ripping out systems.

Skip C unless you're in genuine crisis mode; it's often a permanent band-aid. D is the right eventual answer but premature without knowing what you're actually fixing.

### Next prompt should include
- Which of these resonates most with your situation?
- Answers to the uncertainties above (especially: which system is most trustworthy, and what's the scope of disagreement?)
- Whether you're solving for "immediate pain" or "long-term stability" — or both
- Any organizational constraints (budget, political dynamics, system uptime requirements)

Once I know these, I can sketch a concrete sequence of steps.