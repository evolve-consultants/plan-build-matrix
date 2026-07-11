**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking

You want a SQL migration that:
1. Adds an `archived_at` timestamp column (nullable) to `projects`
2. Sets `archived_at` to the current time for projects created more than two years ago
3. Identifies verification points before execution

### What I'm unsure of

- **Database system**: PostgreSQL, MySQL, SQL Server, or other? (syntax and timestamp functions differ)
- **Backfill logic**: Should the timestamp reflect when the project *became* old (≈2 years ago), or just mark it as archived now?
- **Created column name**: Is it `created_at`, `created_on`, or something else?
- **Migration framework**: Are you using Rails migrations, Alembic, Flyway, or raw SQL files? (affects syntax slightly)
- **Table size**: How many rows in `projects`? (affects locking behavior and whether you need batching)
- **Constraints**: Are there foreign keys pointing to `projects` that might be affected?

### Here's what a PostgreSQL version looks like (Option A)

```sql
-- Migration: Add archived_at to projects
BEGIN;

-- Add the column
ALTER TABLE projects
ADD COLUMN archived_at TIMESTAMP NULL;

-- Backfill: set archived_at for projects created > 2 years ago
UPDATE projects
SET archived_at = NOW()
WHERE created_at < NOW() - INTERVAL '2 years'
  AND archived_at IS NULL;

COMMIT;
```

**Why this structure**: wraps in a transaction so it either fully succeeds or fully rolls back. The `archived_at IS NULL` guard prevents re-marking if the migration runs twice.

### Alternatives I considered

**Option B** (if you want to backfill with the actual age threshold date, not "now"):
```sql
UPDATE projects
SET archived_at = created_at + INTERVAL '2 years'
WHERE created_at < NOW() - INTERVAL '2 years'
  AND archived_at IS NULL;
```
Better if you want `archived_at` to reflect when it crossed the 2-year threshold. Worse if you want a clear "we archived this today" record.

**Option C** (if table is very large and you need to avoid locking):
Batch the update in chunks with sleeps between them. More complex but safer on high-traffic tables.

### What you should double-check before running

1. **Confirm the created column name** — run `DESCRIBE projects;` or equivalent and verify the exact column name
2. **Test the backfill query** in a dev environment:
   ```sql
   SELECT COUNT(*) FROM projects 
   WHERE created_at < NOW() - INTERVAL '2 years';
   ```
   This tells you how many rows will be updated. If it's a surprise number, the logic may be wrong.
3. **Check for existing `archived_at` logic** — search the codebase for any existing references to `archived_at`. If it exists elsewhere, this migration might conflict.
4. **Verify the database system** — the syntax above assumes PostgreSQL. MySQL uses `DATE_SUB()`, SQL Server uses `DATEADD()`, etc.
5. **Check table size and activity** — if `projects` is very large (>10M rows) or actively written to during the migration, you may need batching or a maintenance window.
6. **Confirm foreign keys** — run a query to see if anything foreign-keys to `projects.id`. The new column won't break them, but good to know what depends on this table.
7. **Test the migration on a backup** — run it against a copy of production data first and verify the count of updated rows matches expectation.

### Next prompt should include

- Which database system you're using (PostgreSQL/MySQL/other)
- The exact name of the created-at column
- Answers to any of the uncertainties above that apply to your setup
- Whether you want the backfill to use "now" or the actual 2-year threshold date

Once I have these, I can give you the exact migration + a checklist to run through before execution.