# Addressing Multi-System Data Inconsistency

## Start with diagnosis

**Identify the discrepancies:**
- Which specific fields disagree? (contact info, transaction history, account status?)
- How old is each system's data?
- Do discrepancies follow a pattern? (one system always newer, certain fields consistently wrong?)

**Determine the business impact:**
- Which system is causing actual customer problems?
- Are there compliance/financial reporting risks?
- How urgent is this really?

## Quick wins while you plan bigger fixes

- **Designate a source of truth** for now (even if imperfect) so teams stop contradicting each other
- **Document the gaps** so you know what you're working with
- **Create a triage list** of the most critical inconsistencies to resolve first

## Longer-term approach

1. **Pick one high-value area** (e.g., customer contact info) rather than trying to fix everything at once
2. **Build a master data management process** — establish which system owns what data and when updates sync
3. **Add reconciliation checks** to catch new discrepancies automatically
4. **Plan a cleanup** of historical data once you know the rules

## Questions worth asking first

- When did this start? (New system integration gone wrong?)
- Is this technical (sync failures) or process-based (conflicting update rules)?
- Do you have the budget/timeline for a real MDM solution, or need a workaround?

What's creating the biggest headache right now?