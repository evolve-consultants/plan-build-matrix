# SQL Migration: Add archived_at Timestamp

```sql
-- Migration: Add archived_at column to projects table
-- Created: [DATE]
-- Description: Adds soft-delete capability and backfills for old projects

BEGIN TRANSACTION;

-- Step 1: Add the new column
ALTER TABLE projects
ADD COLUMN archived_at TIMESTAMP NULL;

-- Step 2: Create index for query performance
CREATE INDEX idx_projects_archived_at ON projects(archived_at);

-- Step 3: Backfill projects older than 2 years with current timestamp
UPDATE projects
SET archived_at = NOW()
WHERE created_at < NOW() - INTERVAL '2 years'
  AND archived_at IS NULL;

COMMIT;
```

## Pre-Deployment Checklist

Before running this migration, verify:

- [ ] **Backup exists** – Full database backup completed and tested
- [ ] **Data volume** – How many rows will be updated? Run the SELECT first:
  ```sql
  SELECT COUNT(*) FROM projects
  WHERE created_at < NOW() - INTERVAL '2 years';
  ```
- [ ] **Peak hours** – Schedule during low-traffic window (UPDATE locks may impact queries)
- [ ] **Dependent code** – Search codebase for:
  - Queries that select `*` from projects (may need column exclusion)
  - ORM model definitions (add new field)
  - Any business logic assuming all projects are active
- [ ] **Application state** – Is the app deployed to handle the new `archived_at` column?
- [ ] **Rollback plan** – Prepared SQL to revert:
  ```sql
  DROP INDEX idx_projects_archived_at;
  ALTER TABLE projects DROP COLUMN archived_at;
  ```
- [ ] **Monitoring** – Ready to watch for slow queries or connection pool exhaustion
- [ ] **Date interpretation** – Confirm "2 years" uses correct timezone and `NOW()` function

## Additional Considerations

**If the UPDATE is very large (>1M rows):**
```sql
-- Batch the updates to avoid long locks
DO $$
DECLARE
  batch_size INT := 10000;
BEGIN
  WHILE EXISTS (
    SELECT 1 FROM projects
    WHERE created_at < NOW() - INTERVAL '2 years'
      AND archived_at IS NULL
    LIMIT 1
  ) LOOP
    UPDATE projects
    SET archived_at = NOW()
    WHERE ctid IN (
      SELECT ctid FROM projects
      WHERE created_at < NOW() - INTERVAL '2 years'
        AND archived_at IS NULL
      LIMIT batch_size
    );
    COMMIT;
  END LOOP;
END $$;
```

**To verify the backfill worked:**
```sql
SELECT 
  COUNT(*) total,
  COUNT(CASE WHEN archived_at IS NOT NULL THEN 1 END) archived,
  MIN(archived_at) earliest_archived
FROM projects;
```