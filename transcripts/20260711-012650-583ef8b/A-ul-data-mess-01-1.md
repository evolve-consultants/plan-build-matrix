# Start with diagnosis

**First, understand the scope:**
- How much do they actually disagree? (small discrepancies vs. fundamentally different records)
- Which system(s) are authoritative for different data types?
- When did inconsistencies start?
- Are some systems just out of sync, or is the data genuinely conflicting?

# Practical next steps

1. **Pick a single source of truth** for each data category (customer contact info, order history, etc.). This might be your oldest system, your most-used one, or your most reliable one—depends on your situation.

2. **Audit a sample** of records across systems to find patterns:
   - Are updates flowing one direction only?
   - Are there timezone/timing issues?
   - Is one system receiving bad inputs?

3. **Decide on reconciliation:**
   - Can you merge/deduplicate programmatically?
   - Do some conflicts need manual review?
   - What's your tolerance for losing data?

4. **Fix the source** so they don't diverge again:
   - One system as master, others as read-only copies?
   - Real-time sync (APIs, queues)?
   - Regular batch reconciliation?

# The hard question

Before investing heavily in reconciliation: **do you actually need all four systems?** Sometimes consolidating is cheaper than maintaining multiple conflicting sources.

What does the breakdown look like—four completely separate systems, or more like redundant/overlapping ones?