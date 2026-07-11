**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You need a SQL migration that: (1) adds an `archived_at` timestamp column to `projects` (nullable), (2) sets `archived_at` to a specific value for projects created more than two years ago, and (3) identifies what to verify before executing.

<assumptions>
  <project>You're using a migration system (Rails, Alembic, Flyway, or similar) that supports timestamped or numbered migration files. The `projects` table exists and has a creation timestamp (likely `created_at`). The database is PostgreSQL, MySQL, or similar (I'm assuming one; syntax varies).</project>
  <task>You want to mark old projects as archived retroactively without deleting them, and need the timestamp to reflect when they should have been archived (two years ago) or when the migration runs.</task>
  <operator>You own the verification step — I'll flag what to double-check, but you'll confirm facts against your schema and business logic.</operator>
</assumptions>

### What I'm unsure of
- **Database system**: PostgreSQL, MySQL, MariaDB, or other? (Syntax for timestamp functions differs slightly.)
- **Backfill semantics**: Should `archived_at` be set to `created_at + 2 years`, or to `NOW()` (the migration run time)?
- **Index strategy**: Do you need an index on `archived_at` for queries? (Common for filtering active vs. archived projects.)
- **Existing data checks**: Should the migration verify row counts before/after, or just execute?

### Options

| | Approach | Pros | Cons | Best when |
|---|---|---|---|---|
| **A** | Backfill to `created_at + 2 years` | Reflects the logical archive date; consistent per row | Assumes `created_at` exists and is accurate | You want historical accuracy in the timestamp |
| **B** | Backfill to `NOW()` | Simple; consistent migration run time | Loses information about *when* they should have been archived | You only care that old rows are marked, not when |
| **C** | Two-step: add column, then backfill in a separate migration | Easier to roll back; clearer audit trail | Requires two deploys/migrations | You're risk-averse or have a strict change protocol |

### Here's a rough draft (PostgreSQL, Option A)

```sql
-- Migration: add_archived_at_to_projects
-- Created: 2025-01-14

BEGIN;

-- Step 1: Add the column
ALTER TABLE projects ADD COLUMN archived_at TIMESTAMP NULL;

-- Step 2: Backfill for rows older than 2 years
UPDATE projects
SET archived_at = created_at + INTERVAL '2 years'
WHERE created_at < NOW() - INTERVAL '2 years';

-- Step 3: (Optional) Create index for query performance
CREATE INDEX idx_projects_archived_at ON projects(archived_at) WHERE archived_at IS NOT NULL;

COMMIT;
```

**For MySQL/MariaDB**, replace the interval:
```sql
UPDATE projects
SET archived_at = DATE_ADD(created_at, INTERVAL 2 YEAR)
WHERE created_at < DATE_SUB(NOW(), INTERVAL 2 YEAR);
```

### What to double-check before running

1. **Row count impact**: Run a dry-run query to see how many rows will be updated:
   ```sql
   SELECT COUNT(*) FROM projects WHERE created_at < NOW() - INTERVAL '2 years';
   ```
   If this is thousands or more, consider running the backfill in batches to avoid locking.

2. **`created_at` column exists and is not null**: Confirm the column name and that it's universally populated:
   ```sql
   SELECT COUNT(*) FROM projects WHERE created_at IS NULL;
   ```
   If any rows are missing `created_at`, you'll need logic to handle them (skip, use a default, etc.).

3. **Index necessity**: Do your queries filter on `archived_at` or use it in `WHERE` clauses? If not, skip the index creation to save disk space.

4. **Transaction support**: Confirm your database and migration tool support `BEGIN`/`COMMIT`. (Most do; some tools auto-wrap.)

5. **Downtime or locking**: Test on a staging database first. Large updates can lock the table. If `projects` is write-heavy, schedule the migration during low-traffic hours.

6. **Rollback plan**: Ensure you can drop the column if needed:
   ```sql
   ALTER TABLE projects DROP COLUMN archived_at;
   ```

### Recommended path
**Option A with the index**, after confirming:
- The row count from the dry-run query
- That `created_at` is fully populated
- Your query patterns actually use `archived_at`

### Next prompt should include
- Database system (PostgreSQL, MySQL, etc.)
- Whether you want `archived_at` to reflect the archive date (2 years ago) or the migration run time
- Row count from the dry-run query and any performance concerns
- Whether you need the index or want to defer it