**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You have customer information stored in four different systems, they contain conflicting data, and you need a strategy to resolve or manage that. You're looking for direction on how to proceed.

<assumptions>
  <project>These systems likely have different purposes (CRM, billing, support, analytics?) and different update frequencies; some are probably integrated with each other, others isolated</project>
  <task>You want to establish a single source of truth, or at least a clear resolution strategy so downstream processes can work reliably</task>
  <operator>You own the decision-making but may not own all four systems or have full visibility into their architecture yet</operator>
</assumptions>

### What I'm unsure of
- **Which system is authoritative** (or should be)? Is one the source of truth by design, or do they have equal standing?
- **What kinds of conflicts** are most damaging to your business? (missing records, contradictory values, stale data, duplicates?)
- **What's your timeline and risk tolerance?** (quick bandaid vs. proper rebuild; breaking changes acceptable?)
- **How often does customer data change**, and which systems need to stay in sync?

### Options

| | Approach | Best when | Effort |
|---|---|---|---|
| **A: Audit & Designate** | Inventory what each system owns, pick one as source of truth, backfill the others, then enforce sync | You have time to do it right; conflicts are tolerable short-term; you can identify a clear winner | Medium |
| **B: Real-time Sync Layer** | Build/buy a middleware that reads from one system and pushes to the others on every change | You need perfect consistency immediately; the authoritative system is already reliable; conflicts are expensive | High |
| **C: Staged Reconciliation** | Audit → pick a winner → backfill one system at a time while running in parallel with the old state → flip the switch when confident | You need a safe, testable path; your business can tolerate dual-running for weeks; you want to minimize cutover risk | Medium-High |
| **D: Query-Time Resolution** | Leave systems as-is but add a resolution layer (API, dashboard) that fetches from all four and applies a rule (most recent wins, authoritative system wins, majority vote) | You can't afford downtime or rebuilds; you just need consistency where it matters; downstream systems can handle minor delays | Medium |

### Recommendation
**Start with Option A (Audit & Designate)** because:
1. It forces you to understand the problem before you solve it — conflicts often point to broken upstream processes
2. It's reversible and low-risk
3. It unblocks you to move to B, C, or D later with much higher confidence
4. It usually reveals that one system *is* already the intended source of truth; you just haven't formalized it

### Next prompt should include
- Which of these resonates? Or is there a constraint I'm missing?
- Do you know which system *should* be authoritative, or is that part of the problem?
- Are the conflicts data quality issues (bad values) or architecture issues (systems updating independently)?
- How many customer records are we talking about, and what's your appetite for downtime?