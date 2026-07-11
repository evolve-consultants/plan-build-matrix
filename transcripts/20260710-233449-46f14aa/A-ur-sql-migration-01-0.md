# SQL Migration: Add archived_at to projects table

```sql
-- Migration: Add archived_at timestamp to projects
-- Created: [DATE]

BEGIN;

-- Step 1: Add the new nullable column
ALTER TABLE projects ADD COLUMN archived_at TIMESTAMP NULL;

-- Step 2: Backfill archived_at for projects older than 2 years
UPDATE projects
SET archived_at = updated_at
WHERE updated_at < NOW() - INTERVAL '2 years'
  AND archived_at IS NULL;

-- Step 3: Create index for query performance
CREATE INDEX idx_projects_archived_at ON projects(archived_at);

-- Step 4: Optional - Add index on status filters if common
CREATE INDEX idx_projects_archived_at_created_at ON projects(archived_at, created_at);

COMMIT;
```

## ⚠️ Critical Pre-Flight Checks

### Data Integrity
- [ ] **Backup the database** before running (test restore procedure)
- [ ] Verify the `updated_at` column exists and has correct data
- [ ] Check if "older than 2 years" is the correct cutoff for your business logic
- [ ] Confirm no projects should have `archived_at` set that don't match this criteria

### Logic Validation
- [ ] Does `updated_at` accurately represent when a project became inactive?
- [ ] Are there any projects that should NOT be backfilled? (e.g., archived projects that were recently reopened)
- [ ] Should you use `created_at` or `updated_at` instead? (Verify business logic)

### Performance & Locks
- [ ] **Run during maintenance window** - UPDATE locks the table
- [ ] Check row count: `SELECT COUNT(*) FROM projects WHERE updated_at < NOW() - INTERVAL '2 years'`
- [ ] If > 100k rows, consider batching the update:
  ```sql
  -- Batched update (run multiple times)
  UPDATE projects
  SET archived_at = updated_at
  WHERE updated_at < NOW() - INTERVAL '2 years'
    AND archived_at IS NULL
  LIMIT 10000;
  ```

### Application Impact
- [ ] Verify application code doesn't break with `archived_at IS NULL`
- [ ] Update any queries that filter by status to handle the new column
- [ ] Check if any triggers exist that might conflict

### Index Strategy
- [ ] Confirm you need both indexes (may be redundant)
- [ ] Monitor index creation time on large tables
- [ ] Verify column ordering matches your most common queries

## Example: Safer Batched Version

```sql
BEGIN;

ALTER TABLE projects ADD COLUMN archived_at TIMESTAMP NULL;

-- Batch update to avoid long locks
WITH rows_to_update AS (
  SELECT id FROM projects
  WHERE updated_at < NOW() - INTERVAL '2 years'
    AND archived_at IS NULL
  LIMIT 10000
)
UPDATE projects
SET archived_at = updated_at
WHERE id IN (SELECT id FROM rows_to_update);

CREATE INDEX idx_projects_archived_at ON projects(archived_at);

COMMIT;
```

**Run the batched version multiple times** until no rows are updated.