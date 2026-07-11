**Trivial — matrix not applied.** Classified as formatting request because it's a pure syntactic transformation with no ambiguity about intent or constraints.

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