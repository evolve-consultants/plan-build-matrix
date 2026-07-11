**Operating from: Bottom-Right (Build + Quality)**

### Confirming before I proceed

These are the key assumptions I'm acting on. If any are wrong, now is the time to say so:

- You're using a standard PostgreSQL migration framework (likely Rails with `db/migrate/`, Alembic, Flyway, or similar)
- "Two years" means exactly 24 months before today's date
- Rows older than two years should have `archived_at` set to their `created_at` (or another timestamp column); I'm assuming `created_at` unless you specify otherwise
- You want this in a single migration (not split into schema + data steps)
- The backfill should happen **after** the column is added (safer, avoids locking during write)

---

### The artifact

```sql
-- Migration: Add archived_at timestamp to projects table
-- This adds a nullable column and backfills rows older than 2 years

BEGIN;

-- Step 1: Add the nullable column
ALTER TABLE projects
ADD COLUMN archived_at TIMESTAMP NULL;

-- Step 2: Backfill archived_at for rows older than 2 years
UPDATE projects
SET archived_at = created_at
WHERE created_at < NOW() - INTERVAL '2 years'
  AND archived_at IS NULL;

COMMIT;
```

---

### What you should double-check before running

1. **The timestamp column used for backfill**: I used `created_at`. Verify this is the right reference point. If projects have an `updated_at` or another timestamp you should use instead, adjust the backfill `SET` clause.

2. **Definition of "two years"**: Confirm `NOW() - INTERVAL '2 years'` matches your intent. If you need a fixed date (e.g., "before 2022-01-01"), replace `NOW()` with a literal.

3. **Row count impact**: Run this query first to see how many rows will be affected:
   ```sql
   SELECT COUNT(*) FROM projects
   WHERE created_at < NOW() - INTERVAL '2 years';
   ```
   If it's a very large number (millions), the UPDATE may lock the table for a long time. Consider batching with `LIMIT` or doing it asynchronously.

4. **Existing `archived_at` values**: If any rows already have `archived_at` set, the backfill preserves them (`AND archived_at IS NULL`). Verify this is correct — you don't want to overwrite intentional values.

5. **Index strategy**: After this runs, you'll likely want an index on `archived_at` if you're filtering by it. Plan that as a follow-up migration or add it here (outside the `BEGIN/COMMIT`).

6. **Backup/rollback plan**: Have a backup or rollback script ready. The reverse is:
   ```sql
   ALTER TABLE projects DROP COLUMN archived_at;
   ```

---

If the backfill affects millions of rows, let me know and I'll restructure this to batch the UPDATE or split it into a separate post-deployment step.