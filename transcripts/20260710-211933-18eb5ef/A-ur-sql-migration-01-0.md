# SQL Migration: Add archived_at to projects table

```sql
-- Migration: Add archived_at timestamp to projects table
-- Created: [TIMESTAMP]

BEGIN;

-- Step 1: Add the new nullable column
ALTER TABLE projects ADD COLUMN archived_at TIMESTAMP NULL;

-- Step 2: Backfill archived_at for projects older than 2 years
-- Only projects that haven't been updated recently are considered "old"
UPDATE projects
SET archived_at = updated_at
WHERE updated_at < NOW() - INTERVAL '2 years'
  AND archived_at IS NULL;

-- Step 3: Create index for efficient querying
CREATE INDEX idx_projects_archived_at ON projects(archived_at) 
WHERE archived_at IS NOT NULL;

COMMIT;
```

---

## ⚠️ Critical Things to Double-Check Before Running

### 1. **Backup & Testing**
- [ ] Full database backup completed
- [ ] Tested migration on production data snapshot (staging environment)
- [ ] Verified expected number of rows will be updated
  ```sql
  SELECT COUNT(*) FROM projects 
  WHERE updated_at < NOW() - INTERVAL '2 years';
  ```

### 2. **Business Logic Validation**
- [ ] Confirm that `updated_at` is the right column to use (not `created_at`)
- [ ] Verify the 2-year threshold aligns with business requirements
- [ ] Check if any projects should NOT be backfilled (whitelist/exclusions needed?)
- [ ] Confirm no active projects will be incorrectly marked as archived

### 3. **Application Code**
- [ ] All code referencing `projects` table is already merged/deployed
- [ ] No code assumes `archived_at` doesn't exist (would cause errors on old schema)
- [ ] New code that uses `archived_at` is **already deployed** (deploy before migration if needed)

### 4. **Performance Impact**
- [ ] Update query is acceptable for your table size
  - Large tables may need `BATCH UPDATE` approach instead:
    ```sql
    UPDATE projects
    SET archived_at = updated_at
    WHERE updated_at < NOW() - INTERVAL '2 years'
      AND archived_at IS NULL
    LIMIT 10000;
    -- Repeat until no rows affected
    ```
- [ ] Index creation won't lock table for unacceptable duration

### 5. **Deployment Timing**
- [ ] Run during maintenance window if table is large/frequently accessed
- [ ] Monitor application logs during/after migration
- [ ] Have rollback plan ready (drop column if needed)

---

## Alternative: Safer approach for very large tables

```sql
BEGIN;

-- Add column only (no backfill)
ALTER TABLE projects ADD COLUMN archived_at TIMESTAMP NULL;

-- Create index
CREATE INDEX idx_projects_archived_at ON projects(archived_at) 
WHERE archived_at IS NOT NULL;

COMMIT;

-- Backfill in batches (run separately, can be interrupted/retried)
DO $$
BEGIN
  LOOP
    UPDATE projects
    SET archived_at = updated_at
    WHERE updated_at < NOW() - INTERVAL '2 years'
      AND archived_at IS NULL
    LIMIT 5000;
    
    EXIT WHEN NOT FOUND;
    PERFORM pg_sleep(1); -- Brief pause between batches
  END LOOP;
END $$;
```