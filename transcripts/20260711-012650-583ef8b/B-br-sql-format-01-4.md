**Trivial — matrix not applied.** Classified this as a formatting request because there are no unvalidated assumptions: the intent is clear, the scope is defined, and you own verification of the output's readability.

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