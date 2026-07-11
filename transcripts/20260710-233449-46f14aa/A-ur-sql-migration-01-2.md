# SQL Migration: Add archived_at to projects table

```sql
-- Migration: Add archived_at timestamp to projects table
-- Created: [DATE]
-- Purpose: Enable soft-delete functionality for archived projects

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

-- Optional: Create a partial index if you primarily query active projects
-- CREATE INDEX idx_projects_active ON projects(id) WHERE archived_at IS NULL;

COMMIT;
```

## ⚠️ Critical Checks Before Running

### 1. **Data Validation**
```sql
-- How many rows will be affected?
SELECT COUNT(*) as rows_to_archive
FROM projects
WHERE updated_at < NOW() - INTERVAL '2 years';

-- Sample the data that will be backfilled
SELECT id, name, updated_at
FROM projects
WHERE updated_at < NOW() - INTERVAL '2 years'
LIMIT 10;
```

### 2. **Backup & Recovery**
- [ ] Full database backup completed and verified
- [ ] Know how to restore from backup if needed
- [ ] Have downtime window approved if required

### 3. **Application Impact**
- [ ] Verify application code doesn't rely on `archived_at` NOT NULL
- [ ] Check for any triggers or constraints that might be affected
- [ ] Confirm ORM models handle nullable timestamps correctly

```sql
-- Check for existing triggers
SELECT * FROM information_schema.triggers 
WHERE event_object_table = 'projects';
```

### 4. **Query Performance**
```sql
-- Estimate lock time (especially important on large tables)
SELECT pg_size_pretty(pg_total_relation_size('projects'));

-- Check current indexes
SELECT indexname FROM pg_indexes 
WHERE tablename = 'projects';
```

### 5. **Concurrent Activity**
- [ ] Run during low-traffic window if table is large (>10M rows)
- [ ] Check for long-running transactions that might lock the table
- [ ] Verify max_locks_per_transaction is sufficient

### 6. **The "2 years" Definition**
- [ ] Confirm `updated_at` is the right timestamp (vs `created_at`)
- [ ] Verify 2-year threshold matches your business requirements
- [ ] Consider if timezone matters (NOW() uses server timezone)

## Alternative: Safer approach for large tables

```sql
-- For very large tables, backfill in batches to reduce lock time
BEGIN;

ALTER TABLE projects ADD COLUMN archived_at TIMESTAMP NULL;

-- Backfill in chunks to minimize locking
WITH to_archive AS (
  SELECT id FROM projects
  WHERE updated_at < NOW() - INTERVAL '2 years'
  ORDER BY id
  LIMIT 10000
)
UPDATE projects
SET archived_at = updated_at
WHERE id IN (SELECT id FROM to_archive);

COMMIT;

-- Repeat the UPDATE above in separate transactions until all rows are done
```

## Post-Migration Checks

```sql
-- Verify backfill was successful
SELECT 
  COUNT(*) as total_projects,
  COUNT(archived_at) as archived_count,
  COUNT(*) - COUNT(archived_at) as active_count
FROM projects;

-- Confirm index was created
SELECT * FROM pg_stat_user_indexes 
WHERE relname = 'projects';
```