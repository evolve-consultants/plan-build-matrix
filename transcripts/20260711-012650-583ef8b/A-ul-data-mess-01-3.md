# Data Reconciliation Strategy

Start by understanding **why** they disagree—this matters more than the disagreement itself:

## Immediate diagnosis
- **Pick a sample** of conflicting records and trace their journey through systems
- **Map the data flow**: which system is source-of-truth for what? (billing vs. contact info might have different owners)
- **Check timestamps**: which version is actually newer?
- **Look for transformation issues**: does data get reformatted/truncated moving between systems?

## Common culprits
- System A syncs daily, B syncs weekly → B lags
- Manual overrides in one system not reflected in others
- Different validation rules (email formats, phone number standards)
- Deletions that soft-delete in some systems but hard-delete in others

## Next steps

**Short term** (get stable):
1. Designate which system is authoritative *per field* (not per record)
2. Pause or redirect new changes from weaker sources
3. Create a manual review process for conflicts

**Medium term** (build real solution):
- Implement proper data governance: single source of truth + master data management
- Replace ad-hoc syncing with real integration (ETL, API hub, or proper MDM tool)
- Add audit trails so you can see *why* versions differ

**Question for you**: Do you know if one system is meant to be the source of truth, or did these evolve independently?