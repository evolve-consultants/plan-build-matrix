**Trivial — matrix not applied.** Classified this as a formatting task because there are no unvalidated assumptions: the request is explicit, the outcome is objectively verifiable, and nothing downstream depends on reasoning about intent.

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