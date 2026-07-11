**Trivial — matrix not applied.** Classified this as a formatting request because there are no unvalidated assumptions and the output is purely stylistic.

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