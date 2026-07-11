# Start with diagnosis before fixing

**First, understand the scope:**
- How many customers are affected?
- What specific fields disagree? (address, contact info, purchase history, status?)
- Which system is typically most reliable?
- How critical are these discrepancies?

**Then consider practical approaches:**

1. **Pick a source of truth** — usually the most recently updated or most operationally critical system
2. **Build a reconciliation process** — audit what changed when and why
3. **Establish rules** — document which system wins for each data type (e.g., billing address from system A, contact from system B)
4. **One-time cleanup** — merge/deduplicate based on those rules
5. **Ongoing governance** — APIs or syncing to keep them aligned going forward

**Quick wins first:**
- Stop the bleeding: Can you enforce single-system updates temporarily?
- Check obvious causes: Are there integration failures, batch timing issues, or duplicate customers with slight name variations?

**Before a major cleanup:**
- Do stakeholders agree which system is "right"? (Finance might trust accounting system; customer service might trust their CRM)
- Can you test rules on a subset?

What's the business impact of the disagreement right now? That'll help prioritize whether you need a quick patch or full migration plan.