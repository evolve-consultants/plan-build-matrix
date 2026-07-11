# Migration: Add `archived_at` to `projects`

```sql
-- =====================================================
-- Migration: add_archived_at_to_projects
-- =====================================================

BEGIN;

-- 1. Add the nullable column
ALTER TABLE projects
    ADD COLUMN archived_at TIMESTAMPTZ NULL;

-- 2. Backfill: mark rows older than 2 years as archived
-- Adjust `created_at` to whichever column represents "age" for your use case
-- (e.g., updated_at, last_activity_at, closed_at, etc.)
UPDATE projects
SET archived_at = NOW()
WHERE created_at < NOW() - INTERVAL '2 years'
  AND archived_at IS NULL;

-- 3. Optional: index if you'll query/filter on this often
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_projects_archived_at
    ON projects (archived_at);
-- Note: CREATE INDEX CONCURRENTLY cannot run inside a transaction block.
-- If you want the concurrent build, move it outside the BEGIN/COMMIT
-- and run it as a separate statement.

COMMIT;
```

If you want the index built concurrently (recommended for large tables to avoid locking), split it out:

```sql
-- Run separately, NOT in a transaction
CREATE INDEX CONCURRENTLY idx_projects_archived_at ON projects (archived_at);
```

---

## Things to double-check before running

**1. Which timestamp column defines "age"?**
`created_at` may not be the right signal — you might actually want `updated_at`, `last_activity_at`, or a status-change timestamp. Confirm with product/data owner.

**2. Semantics of `archived_at`**
Does setting it to `NOW()` make sense, or should it reflect *when the row actually became archived* (e.g., backfilled with the same value as the cutoff date, or with `created_at + interval '2 years'`)? Using `NOW()` for all backfilled rows means you lose the actual "archived since" info — consider:
```sql
SET archived_at = created_at + INTERVAL '2 years'
```
if you want a more accurate historical value.

**3. Row count / lock impact**
Run `EXPLAIN` or `SELECT COUNT(*)` on the `UPDATE` predicate first. If it's a huge table, a single bulk `UPDATE` can:
- Hold long locks
- Bloat the table (each update is a new row version in Postgres/MVCC)
- Blow up WAL/replication lag

Consider **batching** the backfill (e.g., update in chunks of 10k–50k rows using a loop or `LIMIT` + primary key range) if this is a large/production table.

**4. Triggers / application side effects**
Check if there are triggers, event listeners, or application logic (webhooks, audit logs, cache invalidation) that fire on `UPDATE projects` — a mass update could trigger a flood of side effects unintentionally.

**5. Downstream consumers**
Does any code currently assume `archived_at IS NULL` means "not archived" in ways that could break once this backfill runs? E.g., dashboards, reports, or APIs that will suddenly start filtering out these "newly archived" rows.

**6. Timezone consistency**
Confirm you want `TIMESTAMPTZ` (recommended) vs `TIMESTAMP`, and that `NOW()` behaves as expected in your DB's configured timezone.

**7. Backup / rollback plan**
Since this is a data-mutating migration (not just schema), make sure you have a recent backup or can identify affected rows to reverse (`archived_at = NULL WHERE ...`) if something's wrong.

**8. Concurrent index creation**
If using `CREATE INDEX CONCURRENTLY`, remember it must run **outside a transaction** and can fail without rolling back cleanly — check for invalid indexes afterward (`pg_index.indisvalid`).