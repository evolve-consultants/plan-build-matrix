**Operating from: Bottom-Right (Build + Quality)**

### Confirming before I proceed

These are the key assumptions I'm acting on. If any are wrong, now is the time to say so:

- You're using a standard SQL database (PostgreSQL, MySQL, etc.) — I'll provide PostgreSQL; let me know if you need a different dialect
- The `projects` table exists and has an `id` column as primary key
- "Older than two years" means `created_at` or similar timestamp is more than 2 years ago from today
- You want `archived_at` to be set to the project's `created_at` for backfill (not some other timestamp)
- This is a one-time migration; you're not adding auto-archival logic
- You own verification of which rows actually get backfilled

---

### The migration

```sql
-- Add the archived_at column
ALTER TABLE projects
ADD COLUMN archived_at TIMESTAMP NULL;

-- Backfill: set archived_at to created_at for projects older than 2 years
UPDATE projects
SET archived_at = created_at
WHERE created_at < CURRENT_TIMESTAMP - INTERVAL '2 years'
  AND archived_at IS NULL;
```

---

### What you should double-check before running

1. **Does your `projects` table have a `created_at` column?**  
   If it uses a different timestamp (e.g., `inserted_at`, `date_added`), change the backfill reference accordingly.

2. **What timestamp should `archived_at` actually be?**  
   I assumed `created_at`, but you might want:
   - `CURRENT_TIMESTAMP` (when the migration runs)
   - `updated_at` (last modification time)
   - Some other column
   
   Decide now — backfill is permanent and changing it requires another migration.

3. **Check the row count that will be affected**  
   Run this *before* the UPDATE to see how many rows will be backfilled:
   ```sql
   SELECT COUNT(*) FROM projects
   WHERE created_at < CURRENT_TIMESTAMP - INTERVAL '2 years'
     AND archived_at IS NULL;
   ```
   Does that number match your expectation? If it's wildly high or low, your date math might be off.

4. **Timezone handling**  
   If your database stores timestamps in UTC but `CURRENT_TIMESTAMP` is interpreted in a different timezone, the "2 years ago" boundary might be wrong. Verify timezone settings if you're in a non-UTC environment.

5. **Test on a copy first**  
   If this is production, run it on a staging clone to confirm the backfill logic and row count before running on live data.