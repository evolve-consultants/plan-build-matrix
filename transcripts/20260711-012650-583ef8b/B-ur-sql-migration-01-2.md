**Operating from: Bottom-Right (Build + Quality)**

### Confirming before I proceed

These are the key assumptions I'm acting on. If any are wrong, now is the time to say so:

- You're using a standard PostgreSQL database (or compatible system like AWS RDS, CloudSQL)
- The `projects` table exists and has an `id` column and a `created_at` timestamp
- "Older than two years" means `created_at < now() - interval '2 years'`
- You want rows matching that condition to have `archived_at` set to their `created_at` value (or another specific timestamp — tell me if different)
- This is a single migration file, not a multi-step rolling deployment
- You own downtime tolerance or have read replicas that can absorb a lock

### The artifact

```sql
-- Migration: Add archived_at to projects table and backfill old records
-- Direction: up

BEGIN;

-- Step 1: Add the column
ALTER TABLE projects ADD COLUMN archived_at TIMESTAMP NULL;

-- Step 2: Backfill rows older than 2 years
-- Sets archived_at to created_at for qualifying records
UPDATE projects
SET archived_at = created_at
WHERE created_at < NOW() - INTERVAL '2 years'
  AND archived_at IS NULL;

COMMIT;
```

### What to double-check before running

1. **Table lock duration**: The `UPDATE` will lock the table. Check row count:
   ```sql
   SELECT COUNT(*) FROM projects WHERE created_at < NOW() - INTERVAL '2 years';
   ```
   If > 100k rows and this is production, consider batching in a separate step (I can show you that if needed).

2. **The two-year cutoff**: Run this to see what you're about to mark:
   ```sql
   SELECT COUNT(*), MIN(created_at), MAX(created_at)
   FROM projects
   WHERE created_at < NOW() - INTERVAL '2 years';
   ```
   Confirm the dates match your intent.

3. **Backfill logic**: Is `archived_at = created_at` the right timestamp, or should it be something else (e.g., the actual archive date from an audit log, or `NOW()`)?

4. **Nullable assumption**: Confirm you want this nullable. If all old rows *must* have a value, change to `NOT NULL DEFAULT now()` instead (though that changes semantics).

5. **Production checklist**:
   - Run on a replica or staging first
   - Have a rollback plan: `ALTER TABLE projects DROP COLUMN archived_at;`
   - If this table is heavily used, schedule during a quiet window
   - Check `pg_stat_activity` during the update to monitor lock contention

6. **Indices**: If you plan to query `WHERE archived_at IS NOT NULL` frequently, consider adding an index after:
   ```sql
   CREATE INDEX idx_projects_archived_at ON projects(archived_at) 
   WHERE archived_at IS NOT NULL;
   ```

---

**What do you need me to adjust?** Let me know if the backfill logic should use a different timestamp or if you need a batched version for a large table.