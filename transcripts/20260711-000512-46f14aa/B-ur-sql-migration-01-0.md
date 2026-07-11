**Operating from: Upper-Right (Build + Verify)**

### What I understand you're asking
Add a nullable `archived_at` timestamp column to `projects`, then backfill it for rows that are more than two years old — likely to mark old projects as archived without deleting them.

<assumptions>
  <project>Postgres syntax; `projects` table exists with a `created_at` column that represents row age; no ORM/migration framework specified, so this is plain SQL you'll drop into whatever tool you use.</project>
  <task>"Older than two years" refers to `created_at`, not `updated_at` or some other field; backfilled value should be `created_at` (i.e., archived_at = when it *would have* been archived) rather than "now."</task>
  <operator>You have permission to run schema changes and updates directly against production, or this goes through a review/CI process before deploy.</operator>
</assumptions>

### The artifact

```sql
-- Migration: add archived_at to projects, backfill rows older than 2 years

BEGIN;

ALTER TABLE projects
  ADD COLUMN archived_at TIMESTAMPTZ NULL;  -- assumed: TIMESTAMPTZ not plain TIMESTAMP

-- Backfill in batches to avoid long-held locks / large single transaction on big tables
-- Adjust batch size based on table size; 10k is a conservative starting point.
DO $$
DECLARE
  rows_updated INT;
BEGIN
  LOOP
    UPDATE projects
    SET archived_at = created_at  -- assumed: backdate to created_at, not NOW()
    WHERE id IN (
      SELECT id FROM projects
      WHERE archived_at IS NULL
        AND created_at < NOW() - INTERVAL '2 years'  -- assumed: created_at is the age reference
      LIMIT 10000
    );
    GET DIAGNOSTICS rows_updated = ROW_COUNT;
    EXIT WHEN rows_updated = 0;
    COMMIT;  -- release lock between batches
  END LOOP;
END $$;

COMMIT;
```

If you don't need batching (small table, low traffic), the whole thing collapses to:

```sql
ALTER TABLE projects ADD COLUMN archived_at TIMESTAMPTZ NULL;

UPDATE projects
SET archived_at = created_at
WHERE created_at < NOW() - INTERVAL '2 years';
```

### What I'm confident about
- `ADD COLUMN ... NULL` is safe and fast in Postgres (no rewrite, no default to backfill).
- Wrapping in a transaction with batched commits avoids long lock waits on large tables.
- Using `archived_at IS NULL` in the batch `WHERE` clause makes the loop idempotent — safe to re-run if it fails partway.

### What I'd double-check
- **Which column defines "older than two years."** If there's an `updated_at`, a soft-delete flag, or a "last activity" field that's more semantically correct for archiving, swap it in — this is the highest-risk assumption.
- **What `archived_at` should actually contain.** I set it to `created_at` (backdated). If you instead want it to mean "the moment this migration archived it," use `NOW()` instead — changes the meaning of the field going forward.
- **Table size.** If `projects` has millions of rows, confirm batch size and consider running the backfill as a separate deploy step (not in the same transaction as the `ALTER TABLE`), so a slow backfill doesn't block deploys.
- **Existing queries/ORM models.** Adding a column is safe, but if any code does `SELECT *` and expects an exact column count/order (some ORMs, some raw drivers), do a quick check.
- **Whether `archived_at` needs an index.** Not included here — add one (`CREATE INDEX CONCURRENTLY`) if you'll be querying/filtering on it often.