**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You have customer records in four different systems with conflicting information, and you need a strategy to resolve this and prevent it from happening again.

<assumptions>
  <project>
    - You're responsible for data quality or integration across these systems
    - The systems aren't designed to sync with each other
    - This affects business operations (billing, support, analytics, etc.)
    - You have some ability to modify processes, data, or system configurations
  </project>
  <task>
    - You want to know how to establish a single source of truth
    - You need a path that doesn't require massive system replacement
    - You probably need to do this without stopping current operations
  </task>
  <operator>
    - You're looking for a practical roadmap, not a complete rebuild
    - You may or may not have engineering resources available
    - You probably need to move quickly but correctly
  </operator>
</assumptions>

### What I'm unsure of
- **Which system should be the source of truth?** Is one system more authoritative or complete than the others? Or do they each own different attributes?
- **How stale is the data?** Are these conflicts old or actively diverging? When did you first notice them?
- **What's the cost of conflict?** Does this cause revenue loss, broken customer experiences, compliance risk, or is it mostly operational friction?
- **Do you have a data integration layer already?** Or are you integrating directly against four separate systems?
- **How many records are affected?** Hundreds, thousands, millions?

### Options

| | Approach | Upside | Downside | Best when |
|---|---|---|---|---|
| **A: Audit & Pick Winner** | Analyze all four systems, pick the most complete/authoritative as source of truth, migrate other systems to reference it. | Clear ownership, simplest mental model, fastest to implement. | Requires identifying a "winner" (may not exist). Doesn't fix root cause of divergence. Data in the other systems may still be correct for their domain. | One system is clearly more authoritative (e.g., billing system owns customer contact; CRM owns engagement data). You have time for a 2-4 week audit. |
| **B: Master Data Management (MDM) Layer** | Build or buy a system (or use a data warehouse) as the single source of truth. Systems feed data in; customers query it from there. | Decouples systems. Gives you a place to store reconciliation rules. Scales to more systems later. | Requires integration work. Adds a dependency. Doesn't immediately fix existing conflicts. | You expect to add more systems in the future, or the four systems serve genuinely different purposes (billing vs. support vs. analytics vs. operations). You have 4-8 weeks and can allocate engineering resources. |
| **C: Phased Reconciliation** | For each system pair, identify conflicts, define rules to resolve them (e.g., "CRM is source of contact info; billing system is source of payment method"), then sync. Repeat across all pairs. | Respects domain boundaries. Teaches you why conflicts exist. Doesn't require picking a "winner." | Slow. Labor-intensive. Requires talking to stakeholders for each rule. | You have time (4-8 weeks+) and conflicts are explainable (e.g., different departments updating different fields). You want to understand the root cause. |
| **D: Immediate Workaround + Long-term Fix** | Deploy a tactical view/API that shows "best guess" customer record (using heuristics and manual overrides) while you plan a deeper solution. | Buys time. Lets operations continue. Gives you space to think. | Doesn't fix the real problem. Workaround can become permanent. | You need to unblock something in the next 1-2 weeks but don't have a complete solution yet. |

### Recommendation
**Start with Option A (audit + pick a winner) as a first pass**, then move to **Option B (MDM layer)** if you find that no single system owns all the data you need.

Here's why: an audit will teach you the shape of the problem and who owns what. Even if you end up building an MDM layer, that knowledge is essential and saves you from building the wrong thing. A one-week audit costs almost nothing and de-risks the next decision.

### Next prompt should include
- Answers to the five uncertainties above
- Who owns each system (billing, support, marketing, etc.)?
- When did conflicts first become visible?
- How are these systems currently integrated (API, batch sync, manual entry)?

Once I know these, I can give you a specific audit roadmap or walk you through the MDM layer design.