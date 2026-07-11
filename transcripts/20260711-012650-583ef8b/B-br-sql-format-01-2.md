**Trivial — matrix not applied.** Classified as a code formatting request with no unvalidated assumptions (straightforward syntactic transformation, no context needed).

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