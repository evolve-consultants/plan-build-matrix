**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You have customer records duplicated or distributed across four separate systems, with inconsistencies between them (different addresses, phone numbers, account statuses, etc.), and you need a strategy to resolve this.

<assumptions>
  <project>You likely have a production environment still running on these four systems, so any solution needs to handle ongoing operations. The systems probably can't all be shut down at once. You may not have perfect audit trails showing which record is "correct" for disputed fields.</project>
  <task>Your goal is probably to establish a single source of truth for customer data — either by consolidating into one system or by implementing a master data hub. You want to know the order of operations and what to prioritize.</task>
  <operator>You're likely a technical leader or architect (not someone at the typing-keys level of a single system), and you're looking for a framework more than implementation details.</operator>
</assumptions>

### What I'm unsure of
- **Scale**: Are we talking 100 customers or 100,000? This changes the economics of manual vs. automated reconciliation.
- **Criticality**: How harmful is it today that they disagree? (Lost revenue? Customer frustration? Compliance risk?) This determines urgency and acceptable cost.
- **Ownership**: Does each system have a "business owner" who controls when it changes? Or is there one team that could enforce a cutover?
- **Audit trail**: Do the systems log *when* records were last modified? That often reveals which one is actually authoritative.
- **Future state**: Are you consolidating into one system, or keeping four but syncing through a master hub?

### Options

| | Upside | Downside | Best when |
|---|---|---|---|
| **A: Audit-first reconciliation** | Establishes truth before action. Catches data quality issues. Builds organizational consensus on rules. | Slow. Requires manual review for conflicts. Doesn't fix the live problem immediately. | Data quality is acceptable enough to live with short-term inconsistency. You have 2-4 weeks. Conflicts are complex (not just duplicates). |
| **B: Master-first (hub pattern)** | Fixes the live problem quickly. Keeps all four systems running. New writes go to master, systems sync from it. | Creates a new dependency. Adds operational complexity. Doesn't fix historical data. | You need to keep all four systems alive for operational reasons. You're okay with a phased fix (historical data cleaned up later). |
| **C: Single system cutover** | Simplest eventual state. One source of truth eliminates future conflicts. | High risk. Requires all four systems to go read-only during migration. Expensive if one system is critical. | You already know which system is the "keeper." You can coordinate a maintenance window. You're willing to accept 4-8 hour downtime. |
| **D: Hybrid (audit + hub)** | Fixes live problem (B) while building toward single source (A). | Most complex. Longest timeline. Requires careful sequencing. | Data quality issues are severe and need fixing. You can't afford downtime. You have 2-3 months. |

### Recommendation
**Start with Option A (audit-first) in a bounded way**, running parallel to Option B (master hub setup).

Here's why: You likely don't yet know *why* they disagree. Until you do, any consolidation risks baking in the wrong data. A quick audit (1-2 weeks, sampling 100-200 customer records across all four systems) reveals:
- Which system is most authoritative (fewer errors, most recent updates)
- Which conflicts are "easy" (duplicates) vs. "hard" (genuinely contradictory business decisions)
- Whether the problem is scope (missing customers in some systems) or accuracy (same customer, different data)

Meanwhile, start designing the master hub so that when audit findings land, you're ready to implement without delay.

### Next prompt should include
- Scale (how many customers?)
- Current pain level (what breaks when they disagree?)
- Can you do a 4-8 hour maintenance window, or must you stay live?
- Do you already suspect which system is most "correct"?