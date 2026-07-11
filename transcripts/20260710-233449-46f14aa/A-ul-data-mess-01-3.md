# Start with diagnosis

**Understand the scope first:**
- How different are they? (small discrepancies vs. fundamentally conflicting records)
- Which system is authoritative, if any?
- When did they last align?
- Are differences in all records or specific customer segments?

# Practical next steps

**Pick your source of truth**
- Choose one system as primary (usually the oldest/most complete, or your official CRM)
- Document why you chose it
- This prevents endless circular debates

**Do a structured reconciliation**
- Run data quality reports comparing each system
- Categorize issues: duplicates, missing fields, conflicting values, stale data
- Quantify: 5% differences vs. 50% matters for urgency
- Map which system is most accurate per data type (might differ)

**Fix the root causes**
- Are integrations failing silently?
- Do people enter data in multiple places?
- Are there conflicting business rules across systems?
- Is one system simply neglected?

**Establish governance going forward**
- Single entry point for key data (one system owns "customer name"?)
- Regular syncs with conflict resolution rules
- Someone responsible for data quality

# The hard part

You may need to decide: consolidate systems (expensive), better integrate them (medium effort), or accept parallel records with documented ownership.

What's your situation—is this a recent discovery or a long-standing problem?