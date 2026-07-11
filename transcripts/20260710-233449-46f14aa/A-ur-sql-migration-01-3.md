# SQL Migration: Add archived_at to projects table

```sql
-- Migration: Add archived_at timestamp to projects table
-- Created: [DATE]
-- Description: Adds soft-delete capability and backfills archived_at for old projects

BEGIN;

-- Step 1: Add the new nullable column
ALTER TABLE projects ADD COLUMN archived_at TIMESTAMP NULL;

-- Step 2: Backfill archived_at for projects older than 2 years
-- This marks projects as archived if they haven't been updated in 2 years
UPDATE projects
SET archived_at = CURRENT_TIMESTAMP
WHERE updated_at < CURRENT_TIMESTAMP - INTERVAL '2 years'
  AND archived_at IS NULL;

-- Step 3: (Optional) Add index for query performance
CREATE INDEX idx_projects_archived_at ON projects(archived_at) 
WHERE archived_at IS NOT NULL;

-- Step 4: (Optional) Add index for filtering active projects
CREATE INDEX idx_projects_active ON projects(archived_at, updated_at) 
WHERE archived_at IS NULL;

COMMIT;
```

---

## ⚠️ Critical Things to Double-Check Before Running

### 1. **Data Integrity**
- [ ] Verify the `updated_at` column exists and contains valid timestamps
- [ ] Check if there are NULL values in `updated_at` (they won't be backfilled)
  ```sql
  SELECT COUNT(*) FROM projects WHERE updated_at IS NULL;
  ```

### 2. **Impact Assessment**
- [ ] Count how many projects will be marked as archived:
  ```sql
  SELECT COUNT(*) FROM projects 
  WHERE updated_at < CURRENT_TIMESTAMP - INTERVAL '2 years';
  ```
- [ ] Verify this number makes sense for your business logic

### 3. **Application Code**
- [ ] Ensure your application's queries filter out archived records where needed
- [ ] Check if `SELECT * FROM projects` queries will break with the new column
- [ ] Verify ORM models/migrations are prepared for the new column

### 4. **Existing Logic**
- [ ] Check if any scheduled jobs or ETL processes reference these "old" projects
- [ ] Confirm the 2-year threshold aligns with your business retention policy
- [ ] Look for any views or materialized views that might be affected

### 5. **Testing**
- [ ] Run on a staging environment first
- [ ] Test that your archival queries work:
  ```sql
  SELECT COUNT(*) FROM projects WHERE archived_at IS NOT NULL;
  SELECT COUNT(*) FROM projects WHERE archived_at IS NULL;
  ```

### 6. **Performance**
- [ ] Check table size before running on production
- [ ] Consider running during low-traffic hours if table is large (>10M rows)
- [ ] Verify `updated_at` index exists for efficient WHERE clause

### 7. **Reversibility**
- [ ] Have a rollback plan if needed:
  ```sql
  DROP INDEX IF EXISTS idx_projects_archived_at;
  DROP INDEX IF EXISTS idx_projects_active;
  ALTER TABLE projects DROP COLUMN archived_at;
  ```

---

## Optional Enhancements

**Add a trigger to auto-archive stale projects:**
```sql
CREATE OR REPLACE FUNCTION auto_archive_old_projects()
RETURNS void AS $$
BEGIN
  UPDATE projects
  SET archived_at = CURRENT_TIMESTAMP
  WHERE updated_at < CURRENT_TIMESTAMP - INTERVAL '2 years'
    AND archived_at IS NULL;
END;
$$ LANGUAGE plpgsql;
```

**Add a constraint to prevent invalid data:**
```sql
ALTER TABLE projects 
ADD CONSTRAINT check_archive_dates 
CHECK (archived_at IS NULL OR archived_at >= created_at);
```