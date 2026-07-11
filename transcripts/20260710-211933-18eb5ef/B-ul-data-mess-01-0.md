**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You have customer records in four different systems, they contain conflicting information, and you need a strategy to resolve this. You're looking for a direction forward.

<assumptions>
  <project>The four systems likely have different purposes (CRM, billing, support, marketing?) and sync/integration may be limited or broken. You probably can't shut any of them down immediately.</project>
  <task>You want to establish a single source of truth and/or ensure downstream processes (sales, support, billing) use correct data.</task>
  <operator>You own or influence these systems but may not have unlimited engineering budget. Data quality is causing real friction.</operator>
</assumptions>

### What I'm unsure of
- **Scope of disagreement**: Are we talking about a few fields per customer, or fundamental conflicts (different customer counts, contradictory addresses)?
- **Root cause**: Did these drift over time, or is there active dual-entry happening? Are they supposed to sync and failing?
- **Urgency and risk**: Is this causing customer-facing problems, billing errors, or compliance issues? Or is it more of a operational annoyance?
- **Architecture**: Are these systems you control, vendor systems, or a mix? Can you modify them?
- **Volume**: How many customers, and how many conflicts per customer on average?

### Options

| | Upside | Downside | Best when |
|---|---|---|---|
| **A: Audit-first (pick a source of truth)** | Lowest risk. You map all conflicts, understand the root cause, then decide which system owns each field. Clean data flows from there. | Time-intensive upfront. Doesn't fix the problem immediately. | You have time, conflicts are complex, or you suspect systemic sync issues. High compliance/financial risk. |
| **B: Consolidate into one system now** | Cleanest long-term solution. Pick the best system, migrate all data there, deprecate the others. Single source of truth going forward. | Requires engineering effort. Risky if migration is sloppy. You need a place to migrate *to* that's actually better. | You have engineering capacity and the conflicts are bad enough to justify the work. One system is clearly the right home. |
| **C: Implement a data hub/integration layer** | Reduces immediate pain without touching legacy systems. Acts as a referee between the four sources. Can be incremental. | Adds a new system to maintain. Doesn't solve the root cause — just hides it. | Systems need to stay independent for business/technical reasons. You need a quick fix while planning a longer solution. |
| **D: Fix one system at a time** | Lower risk per iteration. You can prioritize by impact (fix billing first, then support, etc.). | Slow. Doesn't address the core problem if sync/integration is broken. Easy to get stuck in whack-a-mole mode. | Conflicts are isolated to specific systems or use cases. You can identify and fix root causes incrementally. |

### Recommendation
**Start with A (Audit-first) if you haven't done it yet.** 

Why: You can't choose a smart direction until you know what you're dealing with. An audit takes a week or two and will tell you whether this is a sync problem, data-entry problem, or design problem — and that answer determines everything downstream. Plus it gives you the business case for options B or C.

If you've already audited and know the conflicts are real: **B or C depending on your engineering capacity.** B is better long-term. C is better if you need to buy time.

### Next prompt should include
- Which of those uncertainties you can answer right now (especially: What's the root cause? How bad are the conflicts?)
- Whether you've already done a detailed audit
- How much engineering time you can allocate
- Whether any of these systems are non-negotiable (have to stay independent for compliance/vendor reasons)

Once I have those, I can give you a specific audit plan or migration strategy.