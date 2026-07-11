**Operating from: Bottom-Right (Build + Quality)**

### Confirming before I proceed

These are the key assumptions I'm acting on. If any are wrong, now is the time to say so:

- You want validation **only** for the `YYYY-MM-DD` format — no time component, no timezone, no partial dates
- "Real calendar dates" means the function should reject impossible dates (Feb 30, month 13, etc.) and handle leap years correctly
- Return type: `bool` (True if valid, False otherwise)
- You want to verify the edge cases I handle, so I'll list them explicitly after the code

<assumptions>
  <project>General Python; no external dependencies assumed</project>
  <task>Reusable validation function that can be dropped into any codebase</task>
  <operator>You own the verification; I'm focusing on correctness and clarity</operator>
</assumptions>

---

```python
def is_valid_iso8601_date(date_string: str) -> bool:
    """
    Validates strict ISO-8601 dates in YYYY-MM-DD format only.
    
    Args:
        date_string: A string to validate
        
    Returns:
        True if the string is a valid ISO-8601 date, False otherwise
    """
    # Check format: exactly 10 characters, dashes in positions 4 and 7
    if not isinstance(date_string, str):
        return False
    
    if len(date_string) != 10:
        return False
    
    if date_string[4] != '-' or date_string[7] != '-':
        return False
    
    # Extract and validate year, month, day are numeric
    try:
        year_str, month_str, day_str = date_string.split('-')
    except ValueError:
        return False
    
    if not (year_str.isdigit() and month_str.isdigit() and day_str.isdigit()):
        return False
    
    year = int(year_str)
    month = int(month_str)
    day = int(day_str)
    
    # Validate month range
    if month < 1 or month > 12:
        return False
    
    # Days per month (non-leap year baseline)
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    # Leap year logic: divisible by 400, OR (divisible by 4 AND not by 100)
    is_leap = (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0)
    if is_leap:
        days_in_month[1] = 29
    
    # Validate day range for the given month
    if day < 1 or day > days_in_month[month - 1]:
        return False
    
    return True
```

---

### Edge cases handled

| Edge Case | Input | Expected | Reason |
|-----------|-------|----------|--------|
| Non-string input | `None`, `20230115`, `['2023-01-15']` | `False` | Type safety |
| Wrong length | `"2023-1-15"`, `"2023-01-15 "` | `False` | Format must be exactly 10 chars |
| Missing dashes | `"20230115"` | `False` | Dashes must be in positions 4 and 7 |
| Dashes in wrong places | `"2023/01/15"`, `"2023-01_15"` | `False` | Only hyphens allowed |
| Non-numeric components | `"202a-01-15"`, `"2023-0a-15"` | `False` | Year, month, day must all be digits |
| Month 0 | `"2023-00-15"` | `False` | Month must be 1–12 |
| Month 13 | `"2023-13-01"` | `False` | Month must be 1–12 |
| Day 0 | `"2023-01-00"` | `False` | Day must be ≥ 1 |
| February 29 (non-leap) | `"2023-02-29"` | `False` | 2023 is not a leap year |
| February 29 (leap) | `"2024-02-29"` | `True` | 2024 is a leap year |
| February 30 | `"2023-02-30"` | `False` | February never has 30 days |
| April 31 | `"2023-04-31"` | `False` | April has only 30 days |
| Century year (divisible by 100 but not 400) | `"1900-02-29"` | `False` | Not a leap year |
| Century year (divisible by 400) | `"2000-02-29"` | `True` | Is a leap year |
| Valid date | `"2023-12-25"` | `True` | Normal case |
| Valid leap date | `"2020-02-29"` | `True` | Normal leap year case |
| Year 0 | `"0000-01-01"` | `True` | No restriction on year range (adjust if needed) |
| Leading zeros | `"0001-01-01"` | `True` | Valid per ISO-8601 |

If you need to restrict the year range (e.g., 1900–2100), let me know and I'll add that constraint.