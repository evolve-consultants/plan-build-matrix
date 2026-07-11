# SQL Migration: Add archived_at to projects table

```sql
-- Migration: Add archived_at timestamp to projects table
-- Description: Adds soft-delete capability via archived_at timestamp

BEGIN;

-- Step 1: Add the nullable column
ALTER TABLE projects ADD COLUMN archived_at TIMESTAMP NULL;

-- Step 2: Create index for performance (archived_at is commonly filtered)
CREATE INDEX idx_projects_archived_at ON projects(archived_at);

-- Step 3: Backfill archived_at for rows older than 2 years
-- Only marks as archived if not already modified recently
UPDATE projects
SET archived_at = CURRENT_TIMESTAMP
WHERE archived_at IS NULL
  AND created_at < CURRENT_TIMESTAMP - INTERVAL '2 years'
  AND updated_at < CURRENT_TIMESTAMP - INTERVAL '2 years';

-- Step 4: Verify the update
-- Run this separately to check results before committing
-- SELECT COUNT(*) as archived_count FROM projects WHERE archived_at IS NOT NULL;
-- SELECT COUNT(*) as active_count FROM projects WHERE archived_at IS NULL;

COMMIT;
```

## ⚠️ Critical Pre-Flight Checks

### 1. **Backup & Test Environment**
- [ ] Run against a staging/test database first
- [ ] Ensure database backups are current
- [ ] Test with production-like data volumes

### 2. **Business Logic Review**
- [ ] Confirm the 2-year threshold aligns with business requirements
- [ ] Check if any active projects are older than 2 years (edge case)
- [ ] Verify the logic matches your definition of "archived" (both created_at AND updated_at)

### 3. **Application Impact**
- [ ] Review queries that SELECT from projects—will they break with NULL values?
- [ ] Check if any reports or dashboards explicitly expect NULL archived_at
- [ ] Ensure ORM models handle the new nullable field (add to serialization if needed)
- [ ] Look for any NOT NULL constraints elsewhere that reference this

### 4. **Data Validation**
- [ ] Run the UPDATE statement as a dry-run query first:
  ```sql
  SELECT COUNT(*) FROM projects
  WHERE archived_at IS NULL
    AND created_at < CURRENT_TIMESTAMP - INTERVAL '2 years'
    AND updated_at < CURRENT_TIMESTAMP - INTERVAL '2 years';
  ```
- [ ] Verify this count matches expectations
- [ ] Check for any projects that should NOT be archived despite age

### 5. **Performance Considerations**
- [ ] Row count: Will the UPDATE lock the table for too long?
- [ ] If table is large (>10M rows), consider batching:
  ```sql
  -- Batch update to avoid long locks
  UPDATE projects
  SET archived_at = CURRENT_TIMESTAMP
  WHERE archived_at IS NULL
    AND created_at < CURRENT_TIMESTAMP - INTERVAL '2 years'
    AND updated_at < CURRENT_TIMESTAMP - INTERVAL '2 years'
    AND id <= 100000;  -- Process in chunks
  ```
- [ ] Verify index creation won't block reads (use CONCURRENTLY if supported)

### 6. **Dependencies**
- [ ] Check for foreign keys referencing projects
- [ ] Search code for `archived_at` to find any existing references (conflicts)
- [ ] Review any views or materialized views that use projects

### 7. **Deployment Safety**
- [ ] Can this migration be rolled back if needed?
- [ ] Will your deployment window allow for table locks?
- [ ] Is there monitoring in place for long-running queries?

## Optional: Add a constraint or check

```sql
-- Optionally add CHECK constraint if archived_at should be in the past
ALTER TABLE projects ADD CONSTRAINT archived_at_not_future 
  CHECK (archived_at IS NULL OR archived_at <= CURRENT_TIMESTAMP);
```

Run your verification queries separately before the final COMMIT!