**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You want a SQL migration that adds an `archived_at` timestamp column to a `projects` table, marks projects older than two years as archived (by setting that timestamp), and leaves newer projects null. You also want me to flag what could go wrong.

<assumptions>
  <project>Using a standard SQL migration system (Rails, Flyway, Liquibase, or raw SQL scripts); PostgreSQL, MySQL, or similar RDBMS; projects table has a created_at or similar timestamp; no explicit archived status column already exists</project>
  <task>Preparing projects for soft-delete or archival workflow; two-year threshold is a business rule, not arbitrary</task>
  <operator>You're familiar with migrations and can run them; you own database backups and rollback capability</operator>
</assumptions>

### What I'm unsure of

- **Database system**: PostgreSQL, MySQL, SQL Server, or something else? (affects syntax)
- **Definition of "older than two years"**: is it `created_at < NOW() - INTERVAL 2 YEARS`, or do you have a different date column in mind?
- **Row count**: rough size of the projects table? (if huge, backfill strategy matters)
- **Downtime tolerance**: can the migration lock the table briefly, or does it need to be non-blocking?
- **Environment**: are you testing this on a staging replica first, or going straight to production?

### Option A: Simple, blocking migration (safest for small tables)

```sql
ALTER TABLE projects ADD COLUMN archived_at TIMESTAMP NULL;

UPDATE projects 
SET archived_at = CURRENT_TIMESTAMP 
WHERE created_at < CURRENT_TIMESTAMP - INTERVAL '2 years';
```

**Pros**: straightforward, single transaction, easy to understand and verify  
**Cons**: locks the table during backfill; if projects table is large (>1M rows), this could block writes for seconds to minutes  
**Best when**: table is small (<100k rows) or you have a maintenance window

### Option B: Two-phase migration (safer for large tables)

```sql
-- Phase 1: Add the column (non-blocking on most systems)
ALTER TABLE projects ADD COLUMN archived_at TIMESTAMP NULL;

-- Phase 2: Backfill in batches (if needed for your DB system)
UPDATE projects 
SET archived_at = CURRENT_TIMESTAMP 
WHERE created_at < CURRENT_TIMESTAMP - INTERVAL '2 years'
  AND archived_at IS NULL;
```

**Pros**: phase 1 is usually non-blocking; phase 2 can be tuned or skipped if backfill is fast enough  
**Cons**: slightly more complex; requires two deployment steps  
**Best when**: table is large or you're in a low-downtime environment

### What to double-check before running

1. **Backup**: Do you have a recent full backup? (Not optional. Restore it if backfill goes sideways.)

2. **Dry-run the math**: Run this on production data (or a production replica) without committing:
   ```sql
   SELECT COUNT(*) FROM projects 
   WHERE created_at < CURRENT_TIMESTAMP - INTERVAL '2 years';
   ```
   Does the count match what you expect? Are there any anomalies (e.g., projects with created_at in the future)?

3. **created_at existence and type**: Confirm the column exists and is a timestamp:
   ```sql
   SELECT column_name, data_type 
   FROM information_schema.columns 
   WHERE table_name = 'projects' AND column_name = 'created_at';
   ```

4. **Indexes and foreign keys**: Does anything index or reference `created_at`? Do any foreign key constraints point to `projects` by ID? (The migration itself won't break these, but good to know before you deploy archival logic that depends on `archived_at`.)

5. **Application readiness**: Is your app ready to *handle* archived projects? Are there queries that need filtering (`WHERE archived_at IS NULL`)? Running the migration before application code is prepared will create orphaned data.

6. **Lock timeout**: If your database has a lock timeout, how long will the UPDATE take? For PostgreSQL:
   ```sql
   EXPLAIN ANALYZE UPDATE projects 
   SET archived_at = CURRENT_TIMESTAMP 
   WHERE created_at < CURRENT_TIMESTAMP - INTERVAL '2 years';
   ```

7. **Timezone awareness**: Is `created_at` stored in UTC? Is `CURRENT_TIMESTAMP` in UTC? (Misalignment here could backfill the wrong rows.)

### Recommended path

Use **Option A** if the projects table is <100k rows and you have a maintenance window. Otherwise, use **Option B** and stagger phase 2 if needed. Before running either, execute the dry-run count query above and confirm the number makes sense.

### Next prompt should include

- Confirmation of which database system you're using
- The output of the `COUNT(*)` dry-run (so I can spot anomalies)
- Whether you have a maintenance window or need non-blocking migration
- Whether application code is already merged and ready to filter on `archived_at`