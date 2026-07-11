# SQL Migration: Add archived_at to projects table

```sql
-- Migration: add_archived_at_to_projects
-- Description: Add nullable archived_at timestamp and backfill for old projects

BEGIN;

-- 1. Add the new column as nullable
ALTER TABLE projects ADD COLUMN archived_at TIMESTAMP NULL;

-- 2. Backfill archived_at for projects older than 2 years
UPDATE projects
SET archived_at = updated_at
WHERE updated_at < CURRENT_TIMESTAMP - INTERVAL '2 years'
  AND archived_at IS NULL;

-- 3. Optional: Create index for queries filtering by archived_at
CREATE INDEX idx_projects_archived_at ON projects(archived_at)
WHERE archived_at IS NOT NULL;

COMMIT;
```

## Pre-Flight Checklist ✓

**Before running this migration, verify:**

1. **Backup Status**
   - [ ] Recent database backup exists and is tested
   - [ ] Can restore from backup if needed

2. **Data Review**
   - [ ] Run `SELECT COUNT(*) FROM projects WHERE updated_at < CURRENT_TIMESTAMP - INTERVAL '2 years'` to see how many rows will be affected
   - [ ] Spot-check a few records to confirm the 2-year threshold is correct for your use case
   - [ ] Verify `updated_at` column exists and is properly populated

3. **Application Impact**
   - [ ] No active queries or code depend on `archived_at` not existing
   - [ ] Review application code that queries `projects` table
   - [ ] Check if any triggers or constraints might be affected

4. **Performance**
   - [ ] Confirm table size (large tables with millions of rows may need `CONCURRENTLY` or batching)
   - [ ] Run migration during low-traffic window if table is very large
   - [ ] Verify index creation won't block other queries

5. **Business Logic**
   - [ ] Confirm 2-year threshold aligns with your archival policy
   - [ ] Decide: should `archived_at` ever be set to NULL, or should it be immutable?
   - [ ] Consider adding a `archived` boolean column if you need a hard archived/not-archived state

## For Large Tables

If `projects` has millions of rows, consider batching the update:

```sql
-- Batched update to reduce lock contention
DO $$
DECLARE
  batch_size INT := 10000;
  affected INT;
BEGIN
  LOOP
    UPDATE projects
    SET archived_at = updated_at
    WHERE updated_at < CURRENT_TIMESTAMP - INTERVAL '2 years'
      AND archived_at IS NULL
    LIMIT batch_size;
    
    affected := FOUND::int;
    EXIT WHEN affected = 0;
    
    -- Small pause between batches to reduce lock pressure
    PERFORM pg_sleep(0.1);
  END LOOP;
END $$;
```