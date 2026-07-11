**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You have customer records in four separate systems with conflicting data, and you need a strategy to resolve the inconsistencies and establish a single source of truth going forward.

<assumptions>
  <project>You likely have a mix of legacy and modern systems (CRM, billing, support, marketing platforms?). No unified data layer exists yet. The systems probably have different update frequencies and data quality standards.</project>
  <task>You want to know how to audit the discrepancies, pick which system wins, and prevent future drift—but I'm not sure if you need this solved in days or months, or whether you're building a permanent solution or a one-time reconciliation.</task>
  <operator>You have some engineering resources and business context about which data matters most, but probably aren't running a full data migration project yet.</operator>
</assumptions>

### What I'm unsure of
- **Scope of disagreement**: Are we talking about a few fields on a few records, or systemic misalignment across most customer attributes?
- **Root cause**: Did the systems diverge gradually (ongoing sync issues) or all at once (bad migration, no integration)?
- **Urgency and tolerance**: Can you tolerate 2–4 weeks of work, or do you need a quick patch? How much risk can you accept if reconciliation is imperfect?
- **Source of truth**: Do you have a single system that's *known* to be most accurate, or are all four equally suspect?
- **Data criticality**: Which fields matter most? (identity/contact vs. preferences vs. transaction history, etc.)

### Options

| | Upside | Downside | Best when |
|---|---|---|---|
| **A: Audit-first reconciliation** | Understand the problem before acting. Build a detailed conflict report showing which system has which data, by field. Then pick a winner per field (not per record). | Slowest option; doesn't immediately fix queries. Requires engineering effort to profile data. | You have time to do this right and don't want to propagate bad data. Root cause is unknown. |
| **B: Declare a source of truth** | Fast. Pick the system most people trust (usually the oldest, or the one with the best SLAs). Copy it to a central location. Route all new writes there. | Risk: you might be copying errors. No guarantee the "trusted" system is actually most accurate. Existing integrations may break. | You have a system that's genuinely more reliable than others, or the cost of getting it wrong is low. You need a working system *now*. |
| **C: Build a reconciliation layer** | Long-term fix. Create a single customer data platform (CDP) or master data management (MDM) system. Ingest from all four, apply merge rules, expose a unified API. | Expensive and time-consuming. Requires ongoing governance. Doesn't solve the root cause (why systems diverged in the first place). | You're planning multi-year infrastructure work and can justify the investment. You have complex customer journeys across systems. |
| **D: Staged hybrid** | Balance speed and correctness. Do a quick audit (1–2 weeks) to identify the biggest discrepancies and highest-impact fields. Declare winners for those. Live with remaining drift. Return to it later. | Leaves some mess. Requires a follow-up project. Customers might see inconsistencies in lower-priority fields. | You need a working system soon but also want to avoid big mistakes. You can do a follow-up in 3–6 months. |

### Recommendation
**Start with Option D** (staged hybrid), because it:
- Gets you a working source of truth *and* a clearer picture of the problem in parallel
- Lets you fix the most painful inconsistencies first (revenue-affecting fields, identity)
- Buys time to do a proper long-term fix (A or C) without letting problems fester
- Is fast enough to unblock dependent teams while still being thoughtful

**Immediate next step:**
1. Pick the two fields causing the most operational pain (e.g., email, phone, billing address, last purchase date)
2. Sample 100 customer records across all four systems and count the disagreements
3. Note which system "wins" most often for each field
4. That becomes your reconciliation rule for phase 1

### Next prompt should include
- Which system do you trust most, and why?
- What's the top operational problem the mismatched data is causing right now?
- How many customer records are we talking about? (hundreds, millions?)
- Do you have anyone who can write code to audit and copy data, or is this a business decision only?