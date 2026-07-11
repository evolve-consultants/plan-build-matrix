# SQL Migration: Add archived_at timestamp to projects table

```sql
-- Migration: Add archived_at timestamp to projects table
-- Created: [DATE]
-- Description: Adds optional archived_at column and backfills for old projects

BEGIN TRANSACTION;

-- Step 1: Add the nullable archived_at column
ALTER TABLE projects ADD COLUMN archived_at TIMESTAMP NULL;

-- Step 2: Backfill archived_at for projects older than 2 years
UPDATE projects
SET archived_at = CURRENT_TIMESTAMP
WHERE created_at < CURRENT_TIMESTAMP - INTERVAL '2 years'
  AND archived_at IS NULL;

-- Step 3: Optional - Add index for query performance
CREATE INDEX idx_projects_archived_at 
ON projects(archived_at) 
WHERE archived_at IS NOT NULL;

COMMIT;
```

## ⚠️ Critical Pre-Execution Checklist

### 1. **Data Validation**
```sql
-- Count how many rows will be affected
SELECT COUNT(*) as old_projects_count
FROM projects
WHERE created_at < CURRENT_TIMESTAMP - INTERVAL '2 years';

-- Verify your "2 years ago" calculation is correct
SELECT CURRENT_TIMESTAMP - INTERVAL '2 years' as cutoff_date;

-- Check for any existing archived_at values
SELECT COUNT(*) as existing_archived
FROM projects
WHERE archived_at IS NOT NULL;
```

### 2. **Check for Dependencies**
```sql
-- Verify no constraints will be violated
SELECT * FROM information_schema.table_constraints 
WHERE table_name = 'projects';

-- Check for foreign keys referencing this table
SELECT * FROM information_schema.referential_constraints 
WHERE constraint_name LIKE '%projects%';
```

### 3. **Backup & Testing**
- [ ] Create a backup of the database
- [ ] Test migration on a staging environment first
- [ ] Time the UPDATE query: `EXPLAIN ANALYZE UPDATE projects SET...`
- [ ] Check estimated downtime for the UPDATE (can lock table on large datasets)

### 4. **Application Readiness**
- [ ] Confirm application code handles NULL `archived_at` values
- [ ] Verify no queries assume `archived_at` is always populated
- [ ] Check if views/reports need updating for the new column

### 5. **Index Considerations**
- [ ] If `projects` table is very large (>1M rows), consider:
  - Running UPDATE in batches instead
  - Running CREATE INDEX separately/concurrently
- [ ] For PostgreSQL, use `CONCURRENTLY`:
```sql
CREATE INDEX CONCURRENTLY idx_projects_archived_at 
ON projects(archived_at) 
WHERE archived_at IS NOT NULL;
```

### 6. **Alternative: Safer Batched Approach** (for large tables)
```sql
-- Process in smaller batches to avoid locking
DO $$
DECLARE
  batch_size INT := 10000;
  updated_count INT := 0;
  total_count INT;
BEGIN
  SELECT COUNT(*) INTO total_count
  FROM projects
  WHERE created_at < CURRENT_TIMESTAMP - INTERVAL '2 years'
    AND archived_at IS NULL;
  
  RAISE NOTICE 'Processing % rows', total_count;
  
  WHILE updated_count < total_count LOOP
    UPDATE projects
    SET archived_at = CURRENT_TIMESTAMP
    WHERE id IN (
      SELECT id FROM projects
      WHERE created_at < CURRENT_TIMESTAMP - INTERVAL '2 years'
        AND archived_at IS NULL
      LIMIT batch_size
    );
    
    updated_count := updated_count + batch_size;
    RAISE NOTICE 'Updated % of % rows', updated_count, total_count;
  END LOOP;
END $$;
```

## Post-Execution Verification

```sql
-- Verify the migration completed successfully
SELECT 
  COUNT(*) as total,
  COUNT(CASE WHEN archived_at IS NOT NULL THEN 1 END) as archived_count,
  COUNT(CASE WHEN archived_at IS NULL THEN 1 END) as active_count,
  MIN(archived_at) as earliest_archive,
  MAX(archived_at) as latest_archive
FROM projects;
```