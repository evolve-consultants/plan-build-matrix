**Trivial — matrix not applied.** Classified this as a formatting request because no unvalidated assumptions are in play and the desired output is fully specified.

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