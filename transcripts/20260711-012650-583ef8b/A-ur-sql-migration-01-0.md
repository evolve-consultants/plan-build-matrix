# SQL Migration: Add archived_at to projects

```sql
-- Migration: Add archived_at timestamp to projects table
-- Created: [DATE]

BEGIN;

-- Step 1: Add the new column (nullable)
ALTER TABLE projects
ADD COLUMN archived_at TIMESTAMP NULL;

-- Step 2: Backfill archived_at for projects older than 2 years
UPDATE projects
SET archived_at = updated_at
WHERE updated_at < NOW() - INTERVAL '2 years'
  AND archived_at IS NULL;

-- Step 3: Create index for efficient queries
CREATE INDEX idx_projects_archived_at 
ON projects(archived_at) 
WHERE archived_at IS NOT NULL;

COMMIT;
```

## Pre-Flight Checklist ✓

**Before running this migration, verify:**

### Data & Logic
- [ ] **Row count impact**: Check how many rows will be backfilled
  ```sql
  SELECT COUNT(*) 
  FROM projects 
  WHERE updated_at < NOW() - INTERVAL '2 years';
  ```

- [ ] **Timestamp column exists**: Confirm `updated_at` is the correct column to use (not `created_at`)
  ```sql
  SELECT column_name, data_type 
  FROM information_schema.columns 
  WHERE table_name = 'projects' 
  AND column_name IN ('updated_at', 'created_at');
  ```

- [ ] **Business logic**: Confirm that projects inactive for 2+ years should actually be marked as archived

- [ ] **No conflicting logic**: Check if any application code already uses an `archived_at` column or similar

### Performance & Safety
- [ ] **Backup**: Take a full database backup before running
- [ ] **Table size**: Run on a copy first if `projects` table has millions of rows
- [ ] **Lock time**: Update statement could lock the table briefly—run during low-traffic window
- [ ] **Disk space**: Ensure enough space for the new index
- [ ] **Replication lag**: If replicated database, check replication lag is minimal

### Application Readiness
- [ ] **Code deployed**: Application code that reads `archived_at` is already deployed
- [ ] **NULL handling**: Verify your app handles NULL values correctly (non-archived projects)
- [ ] **Queries updated**: Any queries filtering on archive status are ready
- [ ] **Tests passing**: Related tests pass against the schema change

## Alternative: Two-Step Rollout (Safer)

If you want to reduce risk:

```sql
-- Migration 1: Add column only
BEGIN;
ALTER TABLE projects ADD COLUMN archived_at TIMESTAMP NULL;
CREATE INDEX idx_projects_archived_at ON projects(archived_at) WHERE archived_at IS NOT NULL;
COMMIT;

-- Migration 2: Backfill in batches (run separately after app code deployed)
BEGIN;
UPDATE projects
SET archived_at = updated_at
WHERE updated_at < NOW() - INTERVAL '2 years'
  AND archived_at IS NULL
LIMIT 10000; -- Batch if very large table
COMMIT;
```

This lets you deploy the schema independently from the data migration.