**Trivial — matrix not applied.** Classified this as a formatting request because the intent is clear, no assumptions about intent/context apply, and the output is purely mechanical.

```sql
SELECT
    id,
    name,
    email
FROM
    users
WHERE
    active = 1
    AND created_at > '2025-01-01'
ORDER BY
    name
```