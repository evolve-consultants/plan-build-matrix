**Trivial — matrix not applied.** Classified this as a formatting request because there are no unvalidated assumptions in play and no downstream decisions depend on the answer.

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