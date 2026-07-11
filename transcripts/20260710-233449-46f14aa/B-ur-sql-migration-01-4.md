**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You want a migration that:
1. Adds an `archived_at` timestamp column (nullable) to `projects`
2. Sets `archived_at` to a specific value for projects created before two years ago
3. Identifies what you should verify before executing it

<assumptions>
  <project>
    - You're using a standard Rails migration system (or similar timestamped migration framework)
    - The `projects` table has a `created_at` column to determine "older than two years"
    - You're targeting a production database and want to be cautious
    - The table is large enough that this matters (if it's tiny, some precautions are overkill)
  </project>
  <task>
    - You want to retroactively mark old projects as archived based on age, not current state
    - The backfill should be automatic as part of the migration
  </task>
  <operator>
    - You're familiar with reading migrations but want help identifying verification steps
    - You own the decision about what timestamp value to use for backfilled rows
  </operator>
</assumptions>

### What I'm unsure of
- **Backfill logic**: Should backfilled rows get `archived_at = created_at + 2 years`? Or a fixed date (e.g., "today")? Or something else?
- **"Older than two years"**: Exactly two years ago (`NOW() - INTERVAL '2 years'`) or a softer boundary?
- **Table size**: Roughly how many rows in `projects`? (Affects whether you need to batch the update or add an index first.)
- **Downtime tolerance**: Can the migration lock the table for a few seconds, or does this need to be online-safe?

### Options

| | Backfill value | Upside | Downside | Best when |
|---|---|---|---|---|
| **A** | `created_at + 2 years` | Marks the moment each project would have aged out; historially accurate | Requires a calculation; might be confusing if the column is meant to track "when we actually archived it" | You want the column to represent the *theoretical* archive date based on age |
| **B** | `NOW()` (execution time) | Simple; one value for all backfilled rows; clear "migration ran" signal | Loses the original cutoff date; all old projects appear to have been archived at the same moment | You want to mark "this migration ran" and don't need historical precision |
| **C** | `NULL` (no backfill; manual decision) | No risk of wrong data; forces explicit review of each project | Leaves the column empty for old projects; requires a follow-up manual process | You want to decide case-by-case which old projects to archive |

### Recommendation
**Option A** (backfill with `created_at + 2 years`) because it's the most defensible: it creates a clear, auditable rule ("anything created >2 years ago is marked as archived at that threshold") and survives a code review. If someone asks "why is this project archived?", you have an answer.

**However**, before I write the migration, you should confirm:
1. Do you actually want to *backfill* old projects, or just add the column and decide what to do with it later?
2. What should the backfill timestamp be — and why?
3. How many rows are we talking about?

### Next prompt should include
- Which option you prefer
- Answers to the three questions above
- Whether the `projects` table is indexed on `created_at` (or if you know its size)

---

Once you confirm, I'll give you the full migration SQL plus a concrete checklist of things to verify before running it.