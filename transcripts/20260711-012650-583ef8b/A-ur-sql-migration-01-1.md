# SQL Migration: Add archived_at to Projects Table

```sql
-- Migration: Add archived_at timestamp to projects table
-- Created: [DATE]

BEGIN;

-- Step 1: Add the new nullable column
ALTER TABLE projects
ADD COLUMN archived_at TIMESTAMP NULL;

-- Step 2: Backfill archived_at for projects older than 2 years
UPDATE projects
SET archived_at = updated_at
WHERE updated_at < NOW() - INTERVAL '2 years'
AND archived_at IS NULL;

-- Step 3: Create index for query performance
CREATE INDEX idx_projects_archived_at ON projects(archived_at)
WHERE archived_at IS NOT NULL;

COMMIT;
```

## Pre-Migration Checklist

✅ **Critical Checks:**

1. **Backup your database** - Create a full backup before running
2. **Verify table name** - Confirm `projects` table exists and is the correct one
3. **Check row count** - See how many rows will be updated:
   ```sql
   SELECT COUNT(*) 
   FROM projects 
   WHERE updated_at < NOW() - INTERVAL '2 years';
   ```
4. **Review update logic** - Confirm `updated_at` is the right field for determining "older than 2 years"
5. **Check for NULL values** - Verify if `updated_at` has NULLs that might cause issues:
   ```sql
   SELECT COUNT(*) 
   FROM projects 
   WHERE updated_at IS NULL;
   ```
6. **Test on staging** - Run this exact migration on a production-like database first
7. **Plan for downtime** - On large tables (millions of rows), the UPDATE may lock the table. Consider:
   - Running during off-peak hours
   - Breaking the UPDATE into batches if needed (see alternative below)
8. **Verify column doesn't exist** - Ensure no `archived_at` column already exists
9. **Review index usage** - Confirm you'll actually query by `archived_at`

## Alternative: Batch Update (for Large Tables)

If your projects table is very large, batch the updates to avoid long locks:

```sql
BEGIN;

ALTER TABLE projects
ADD COLUMN archived_at TIMESTAMP NULL;

-- Update in chunks to avoid locking
DO $$
DECLARE
    v_updated INT := 1;
BEGIN
    WHILE v_updated > 0 LOOP
        UPDATE projects
        SET archived_at = updated_at
        WHERE updated_at < NOW() - INTERVAL '2 years'
        AND archived_at IS NULL
        LIMIT 10000;
        
        v_updated := ROW_COUNT;
        RAISE NOTICE 'Updated % rows', v_updated;
        COMMIT;
    END LOOP;
END $$;

CREATE INDEX idx_projects_archived_at ON projects(archived_at)
WHERE archived_at IS NOT NULL;

COMMIT;
```

## Post-Migration Verification

```sql
-- Verify the migration worked
SELECT COUNT(*) as total_archived
FROM projects 
WHERE archived_at IS NOT NULL;

-- Check a sample of backfilled rows
SELECT id, updated_at, archived_at, (NOW() - archived_at) as age
FROM projects 
WHERE archived_at IS NOT NULL
LIMIT 10;

-- Verify index was created
SELECT indexname 
FROM pg_indexes 
WHERE tablename = 'projects' 
AND indexname = 'idx_projects_archived_at';
```