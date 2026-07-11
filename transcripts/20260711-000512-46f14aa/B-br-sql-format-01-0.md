**Operating from: Bottom-Right (Build + Quality)**

### Confirming before I proceed
- Keeping column/table names and string literals exactly as given (no case changes to identifiers)
- "Keywords uppercase" applies to SQL keywords only (SELECT, FROM, WHERE, AND, ORDER BY), not identifiers

### The artifact

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