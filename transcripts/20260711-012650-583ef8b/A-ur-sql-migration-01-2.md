# SQL Migration: Add archived_at to projects table

```sql
-- Migration: Add archived_at timestamp to projects table
-- Created: [DATE]

BEGIN;

-- Step 1: Add the new nullable column
ALTER TABLE projects ADD COLUMN archived_at TIMESTAMP NULL;

-- Step 2: Backfill archived_at for projects older than 2 years
UPDATE projects
SET archived_at = updated_at
WHERE updated_at < NOW() - INTERVAL '2 years'
  AND archived_at IS NULL;

-- Step 3: Create index for query performance (optional but recommended)
CREATE INDEX idx_projects_archived_at ON projects(archived_at);

COMMIT;
```

## Things to Double-Check Before Running

### 1. **Data Integrity**
- [ ] Verify the `updated_at` column exists and contains reliable data
- [ ] Check how many rows will be affected: 
  ```sql
  SELECT COUNT(*) FROM projects 
  WHERE updated_at < NOW() - INTERVAL '2 years';
  ```
- [ ] Confirm the cutoff date is correct for your use case

### 2. **Backup & Safety**
- [ ] Ensure recent database backups exist
- [ ] Test on staging/development environment first
- [ ] Consider running outside peak hours
- [ ] Have a rollback plan ready

### 3. **Application Code**
- [ ] Check if any application code explicitly expects `archived_at` to NOT exist
- [ ] Verify application handles the new NULL values correctly
- [ ] Confirm queries don't break with the new column

### 4. **Performance**
- [ ] Check table size: `SELECT pg_size_pretty(pg_total_relation_size('projects'));`
- [ ] If table is very large (>100M rows), consider batching the UPDATE:
  ```sql
  -- Run in smaller batches to avoid locking
  UPDATE projects
  SET archived_at = updated_at
  WHERE updated_at < NOW() - INTERVAL '2 years'
    AND archived_at IS NULL
  LIMIT 10000;
  ```

### 5. **Constraints & Dependencies**
- [ ] Verify no foreign keys reference this column
- [ ] Check for any views or triggers that might be affected
- [ ] Confirm no existing indexes would be invalidated

### 6. **Deployment**
- [ ] Is this migration part of a zero-downtime deployment?
- [ ] Do you need to coordinate with application deployment timing?
- [ ] Will you deploy code before or after the migration?

---

## Alternative: Non-blocking Version for Large Tables

If your `projects` table is very large, consider this non-blocking approach:

```sql
BEGIN;

-- Add column (non-blocking)
ALTER TABLE projects ADD COLUMN archived_at TIMESTAMP NULL;

COMMIT;

-- Backfill in batches (run separately, outside transaction)
DO $$
DECLARE
  rows_updated INT;
BEGIN
  LOOP
    UPDATE projects
    SET archived_at = updated_at
    WHERE updated_at < NOW() - INTERVAL '2 years'
      AND archived_at IS NULL
    LIMIT 10000;
    
    rows_updated := FOUND;
    EXIT WHEN rows_updated = 0;
    
    -- Add delay between batches to reduce load
    PERFORM pg_sleep(0.1);
  END LOOP;
END $$;

BEGIN;

-- Create index (add after backfill completes)
CREATE INDEX idx_projects_archived_at ON projects(archived_at);

COMMIT;
```