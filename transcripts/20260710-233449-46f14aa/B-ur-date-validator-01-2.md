**Operating from: Bottom-Right (Build + Quality)**

### Confirming before I proceed

These are the key assumptions I'm acting on:
- You want validation that rejects malformed strings and impossible dates (Feb 30, etc.)
- "Strict ISO-8601" means YYYY-MM-DD format only — no time, timezone, week notation, or ordinal dates
- You own the verification of correctness; I'm focusing on code quality and completeness
- A simple True/False return is sufficient (not a parsed date object)

---

```python
def is_valid_iso8601_date(date_string: str) -> bool:
    """
    Validate a strict ISO-8601 date in YYYY-MM-DD format.
    
    Args:
        date_string: A string to validate
        
    Returns:
        True if valid, False otherwise
    """
    # Format check: exactly 10 chars, hyphens in right places
    if not isinstance(date_string, str) or len(date_string) != 10:
        return False
    
    if date_string[4] != '-' or date_string[7] != '-':
        return False
    
    # Extract and validate numeric parts
    year_str, month_str, day_str = (
        date_string[0:4],
        date_string[5:7],
        date_string[8:10]
    )
    
    # All parts must be digits
    if not (year_str.isdigit() and month_str.isdigit() and day_str.isdigit()):
        return False
    
    year, month, day = int(year_str), int(month_str), int(day_str)
    
    # Month range
    if not (1 <= month <= 12):
        return False
    
    # Day range (accounting for leap years)
    if month in (1, 3, 5, 7, 8, 10, 12):
        max_day = 31
    elif month in (4, 6, 9, 11):
        max_day = 30
    else:  # February
        is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
        max_day = 29 if is_leap else 28
    
    return 1 <= day <= max_day
```

---

### Edge cases handled

| Edge Case | Behavior | Why |
|---|---|---|
| Wrong type (int, None, list) | Returns False | Type safety |
| Wrong length ("2024-1-1", "2024-01-01 ") | Returns False | Format strictness |
| Wrong separators ("2024/01/01", "2024.01.01") | Returns False | ISO-8601 requires hyphens |
| Non-digit characters ("202a-01-01") | Returns False | All parts must be numeric |
| Month out of range (month 0, 13, 99) | Returns False | 1–12 only |
| Day out of range (day 0, 32) | Returns False | 1–31 (or 1–30/29/28 per month) |
| Invalid day for month (Feb 30, Apr 31) | Returns False | Calendar-aware validation |
| Leap year: Feb 29 in leap year | Returns True | Divisible by 4 (except century years) |
| Leap year: Feb 29 in non-leap year | Returns False | e.g., 2023-02-29 rejected |
| Century leap year (2000) | Returns True | Divisible by 400 |
| Century non-leap year (1900) | Returns False | Not divisible by 400 |
| Leading zeros ("2024-01-01") | Returns True | Required by ISO-8601 |
| Single-digit month without leading zero ("2024-1-01") | Returns False | Strictness |
| Year 0000 or negative | Returns True (if formatted) | No validation on year range; adjust if needed |

### Test it with

```python
assert is_valid_iso8601_date("2024-01-01") == True
assert is_valid_iso8601_date("2024-02-29") == True   # leap year
assert is_valid_iso8601_date("2023-02-29") == False  # not a leap year
assert is_valid_iso8601_date("2024-13-01") == False  # invalid month
assert is_valid_iso8601_date("2024-01-32") == False  # invalid day
assert is_valid_iso8601_date("2024/01/01") == False  # wrong separator
assert is_valid_iso8601_date("2024-01-01 ") == False # trailing space
assert is_valid_iso8601_date("2024-1-01") == False   # no leading zero
assert is_valid_iso8601_date(2024) == False          # not a string
```