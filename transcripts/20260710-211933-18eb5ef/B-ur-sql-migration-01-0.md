**Operating from: Bottom-Right (Build + Quality)**

### Confirming before I proceed

These are the key assumptions I'm acting on. If any are wrong, now is the time to say so:

- You're using a PostgreSQL-compatible database (or I should adjust the syntax)
- The `projects` table exists and has an `id` column and a timestamp column (likely `created_at`) to measure age
- "Older than two years" means rows where `created_at < now() - interval '2 years'`
- You want `archived_at` to be set to `created_at` for those rows (not to the current timestamp)
- This is a single migration file in a standard migration framework (Rails, Alembic, Flyway, etc.)
- The table is not so large that adding a column will cause locking issues in production

---

### The migration

```sql
-- Add nullable archived_at column
ALTER TABLE projects ADD COLUMN archived_at TIMESTAMP NULL;

-- Backfill for rows older than 2 years
UPDATE projects
SET archived_at = created_at
WHERE created_at < NOW() - INTERVAL '2 years';
```

---

### What to double-check before running

1. **Column name for age calculation**: Confirm the timestamp column you're measuring against is actually `created_at`. If it's named something else (`date_created`, `inserted_at`), adjust the `WHERE` clause.

2. **Backfill logic**: Decide what timestamp `archived_at` should hold for old rows. I've set it to `created_at`, which marks them as "archived as of when they were created" — a historical marker. If you want it to reflect "archived right now," use `NOW()` instead. If there's a different logical timestamp (like `updated_at`), use that.

3. **Table size and downtime tolerance**: If `projects` is very large (millions of rows), the `UPDATE` may lock the table for several seconds or minutes. Check row count first with `SELECT COUNT(*) FROM projects`. If it's huge and production can't tolerate downtime, consider batching the update in smaller chunks with a loop.

4. **Timezone**: Confirm that `NOW()` in your database is set to the timezone you expect. If `created_at` is stored in UTC but you want "2 years ago" measured in a different timezone, adjust accordingly.

5. **Index impact**: Adding a column doesn't require an index, but if you plan to query by `archived_at` frequently, you'll want to add one afterward:
   ```sql
   CREATE INDEX idx_projects_archived_at ON projects(archived_at);
   ```

6. **Backup**: Run a backup before executing in production, even if it's low-risk. The backfill is idempotent (running it twice won't hurt), but the column add is not.

7. **Test the WHERE clause first**: Before the full migration, run `SELECT COUNT(*) FROM projects WHERE created_at < NOW() - INTERVAL '2 years'` to see how many rows will be affected. This gives you confidence that the backfill scope is what you expect.