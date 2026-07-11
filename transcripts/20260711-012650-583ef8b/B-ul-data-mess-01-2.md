**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You have customer records in four different systems with conflicting data, and you need a strategy for resolving or consolidating them. You're probably asking how to prioritize the fix and what the actual steps should be.

<assumptions>
  <project>These are separate operational systems (CRM, billing, support, analytics?) that likely evolved independently. Data conflicts are probably at the record level (same customer ID, different addresses/emails) or at the identity level (same person registered under different IDs).</project>
  <task>You need to either: reconcile the systems so they agree going forward, pick a single source of truth, or build a layer that resolves conflicts on the fly. The urgency probably depends on whether this is causing customer-facing problems or just operational friction.</task>
  <operator>You're asking for direction, which suggests you haven't done a full audit yet and need help deciding where to start.</operator>
</assumptions>

### What I'm unsure of
- **Scale**: Are we talking hundreds of conflicts or millions? (determines whether manual review is even feasible)
- **Root cause**: Is this from bad integration, data decay over time, duplicate account creation, or migrations that didn't de-dupe?
- **Urgency**: Is this causing live problems (customers seeing wrong data, billing errors) or is it a technical debt issue?
- **Authority**: Can you change all four systems, or are some owned by other teams/vendors?
- **Tolerance for downtime**: Do these systems need to stay live while you fix this?

### Options

| | Approach | Upside | Downside | Best when |
|---|---|---|---|---|
| **A: Audit first, then consolidate** | Full data inventory of conflicts. Pick a source of truth. Migrate/merge records. Update systems incrementally. | Clear picture of the problem before spending money. Lowest risk of making it worse. | Slowest to see results. High manual effort upfront. | You don't know how bad it is, or conflicts are high-stakes (billing/legal data). |
| **B: Single source of truth + sync layer** | Designate one system as canonical. Build real-time or batch sync to others. Accept minor lag in non-canonical systems. | Can ship fast. Existing systems keep working. Future conflicts are automatically resolved. | Still requires initial reconciliation of historical data. Ongoing sync maintenance. | You have one system that's more reliable/authoritative, and you can accept eventual consistency. |
| **C: Customer data platform (CDP)** | Implement a dedicated deduplication/identity layer (custom or off-the-shelf). Feed all four systems from it. | Clean break from legacy data. Scales well. Can be sold internally as "single customer view." | Expensive. Adds a new system to maintain. Requires rework of all four integrations. | This is a growing headache and you want to future-proof, or you have budget. |
| **D: Triage and isolate** | Fix only the conflicts that matter (customer-facing, revenue-impacting). Leave the rest alone. Document the gap. | Minimal effort. Fast wins. | Technical debt stays. Doesn't solve the root cause. | You have limited time/budget and this is a temporary business problem. |

### Recommendation
**Start with a lightweight audit (Option A, phase 1)** because:
1. You can't decide on a fix without knowing the shape of the problem
2. The audit itself might reveal that one system is already more authoritative than you think
3. A small audit (<1 week) unblocks conversations with other teams about who owns what
4. Once you have numbers, Options B or C become much clearer

After the audit, you'll likely land on **Option B** (single source of truth + sync) for most teams — it's the pragmatic middle ground.

### What the audit should include
- How many customers have conflicting records? (Pick a key field: email, phone, primary ID)
- Which system has the most "correct" data for each field? (Ask the teams that use it)
- Are conflicts from duplicate accounts or from stale sync?
- Which conflicts are causing real problems vs. just being annoying?

### Next prompt should include
- Which of these sounds closest to your situation (or is it something different?)
- What's driving this now — a specific incident or just accumulated pain?
- Do you have time/budget to run a formal audit, or do you need to move faster?
- Who owns each of the four systems?