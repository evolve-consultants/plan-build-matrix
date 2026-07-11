**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You want a SQL migration that:
1. Adds an `archived_at` timestamp column (nullable) to `projects`
2. Sets `archived_at` to a specific value for projects created before two years ago
3. I flag what needs verification before you run it

### What I'm unsure of

- **Database system**: PostgreSQL, MySQL, SQL Server, or something else? (affects syntax and timestamp functions)
- **Backfill logic**: Should `archived_at` be set to the project's `created_at`, to "two years ago", to "now", or to something else?
- **Table structure**: Do you have a `created_at` column? Any other timestamp columns I should know about?
- **Environment**: Is this a high-traffic table where locking during migration matters? Do you have downtime windows?
- **Rollback strategy**: Do you need the ability to safely roll back, or is this one-way?

### Option A: PostgreSQL, backfill to created_at
```sql
-- Step 1: Add the column
ALTER TABLE projects ADD COLUMN archived_at TIMESTAMP NULL;

-- Step 2: Backfill rows older than 2 years
UPDATE projects 
SET archived_at = created_at
WHERE created_at < NOW() - INTERVAL '2 years'
  AND archived_at IS NULL;
```

**Upside**: Simple, clear intent. `created_at` as the archived timestamp makes sense if "old = should have been archived".  
**Downside**: If created_at is very old, archived_at will be very old too (may be semantically odd).

### Option B: PostgreSQL, backfill to "now"
```sql
ALTER TABLE projects ADD COLUMN archived_at TIMESTAMP NULL;

UPDATE projects 
SET archived_at = NOW()
WHERE created_at < NOW() - INTERVAL '2 years'
  AND archived_at IS NULL;
```

**Upside**: All backfilled projects show "archived today" — useful for sorting recent changes.  
**Downside**: Loses the information about *when* they should have been archived.

### Option C: PostgreSQL with explicit two-year cutoff date
```sql
ALTER TABLE projects ADD COLUMN archived_at TIMESTAMP NULL;

UPDATE projects 
SET archived_at = NOW() - INTERVAL '2 years'
WHERE created_at < NOW() - INTERVAL '2 years'
  AND archived_at IS NULL;
```

**Upside**: Archives them "at the cutoff point" — all backfilled projects share the same timestamp, making them easy to identify later.  
**Downside**: Slightly artificial.

### Recommendation
**Option A** (backfill to `created_at`) because it preserves the actual creation date and is most defensible in an audit. If you need to know when projects *became* archived, you can add a comment in the migration explaining the backfill policy.

But I need to confirm:
1. **Database system** — are you on PostgreSQL? (changes syntax)
2. **Backfill intent** — which timestamp makes sense in your domain?
3. **Table size & traffic** — do you need `CONCURRENTLY` or batching?

### What to double-check before running

- [ ] Does `projects` have a `created_at` column? (If not, backfill logic changes)
- [ ] Is this PostgreSQL, MySQL, or other? (Syntax varies; `NOW()` vs `CURRENT_TIMESTAMP` vs `GETDATE()`)
- [ ] How many rows will be backfilled? (If >1M, consider batching to avoid long locks)
- [ ] Is there an index on `created_at`? (If yes, the UPDATE will be faster; if no, consider adding one)
- [ ] Do you have a `NOT NULL` constraint on `created_at`? (If not, the WHERE clause needs adjustment)
- [ ] Are there active writes to `projects` during the migration window? (If yes, lock strategy matters)
- [ ] Do you want to add an index on `archived_at` afterward? (Depends on query patterns)

### Next prompt should include
- Your database system and schema for `projects` (column names, types, constraints)
- What `archived_at` should actually represent in your domain
- Approximate row count and whether you have a maintenance window
- Whether you need a rollback plan