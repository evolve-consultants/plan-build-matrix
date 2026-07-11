# Getting aligned customer data

This is common and fixable. Here's a practical approach:

## Diagnose first
- **Map the systems**: List what each tracks (names, emails, addresses, transaction history, etc.)
- **Find discrepancies**: Pick a sample of customers and see *where* records differ
- **Understand why**: Is it timing (one updates slower)? Different validation rules? User error? System integrations that broke?

## Decide on truth
You'll need a **source of record** for each data type:
- Sometimes it's obvious (your billing system for payment info)
- Sometimes you need a hybrid rule (most recent update wins, or highest-confidence data source)
- Document this explicitly—it prevents future arguments

## Clean and consolidate
- **Deduplicate** across systems (same customer, different records)
- **Standardize format** (consistent phone/address formatting)
- **Reconcile** major discrepancies manually or with rules
- Consider a **master data management (MDM) tool** if you're large enough

## Prevent recurrence
- Choose one system as the primary (if possible)
- Automate syncing between systems
- Add validation rules at entry points
- Regular audits of key fields

## Quick wins to start
- Fix the data causing immediate business problems first
- Don't aim for perfection—aim for "good enough to act on"

What systems are we talking about? That might suggest which ones should be authoritative.