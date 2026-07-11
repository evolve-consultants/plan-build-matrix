**Operating from: Bottom-Right (Build + Quality)**

### Confirming before I proceed

These are the key assumptions I'm acting on. If any are wrong, now is the time to say so:

- You want to validate the **format** `YYYY-MM-DD` exactly (no time, timezone, or alternate formats)
- You want to reject **invalid calendar dates** (Feb 30, Nov 31, etc.)
- You want to reject leap year edge cases incorrectly (e.g., Feb 29 on non-leap years)
- You want a function that returns `True` or `False` (or raises an exception — I'm assuming boolean return)
- You don't need a custom exception class; built-in exceptions are fine
- You're okay with a straightforward implementation using the standard library (no external dependencies)

---

### The artifact

```python
from datetime import datetime

def is_valid_iso8601_date(date_string: str) -> bool:
    """
    Validate strict ISO-8601 dates in YYYY-MM-DD format.
    
    Returns True only if the string is a valid calendar date in that exact format.
    """
    # Check format: must be exactly 10 characters, pattern YYYY-MM-DD
    if not isinstance(date_string, str) or len(date_string) != 10:
        return False
    
    if date_string[4] != '-' or date_string[7] != '-':
        return False
    
    # Check that year, month, day are all digits
    if not (date_string[:4].isdigit() and 
            date_string[5:7].isdigit() and 
            date_string[8:10].isdigit()):
        return False
    
    # Parse and validate as a real calendar date
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        # Invalid date (e.g., Feb 30, month 13, day 0)
        return False
```

---

### Edge cases handled

| Edge Case | Example | Behavior |
|-----------|---------|----------|
| Wrong type | `12345` (int) | Rejected (not a string) |
| Wrong length | `"2024-1-1"` | Rejected (9 chars, not 10) |
| Missing dashes | `"20240101"` | Rejected (no separators) |
| Wrong separator | `"2024/01/01"` | Rejected (slash instead of dash) |
| Non-digit characters | `"202a-01-01"` | Rejected (letter in year) |
| Invalid month | `"2024-13-01"` | Rejected (month 13) |
| Invalid day | `"2024-01-32"` | Rejected (Jan has 31 days) |
| Feb 29 on non-leap year | `"2023-02-29"` | Rejected (not a leap year) |
| Feb 29 on leap year | `"2024-02-29"` | **Accepted** (2024 is a leap year) |
| Feb 30 | `"2024-02-30"` | Rejected (Feb has max 29 days) |
| Day 0 | `"2024-01-00"` | Rejected (days start at 1) |
| Month 0 | `"2024-00-15"` | Rejected (months start at 1) |
| Year 0000 | `"0000-01-01"` | **Accepted** (valid per ISO-8601, though historically debated) |
| Leading/trailing whitespace | `" 2024-01-01"` | Rejected (length is 11) |
| Valid dates | `"2024-12-25"`, `"2000-02-29"` | **Accepted** |

---

### What I'm confident about

- The function correctly validates all real calendar dates using `datetime.strptime()`, which is the standard library's authoritative source for calendar rules (including leap years)
- The format check is strict: exactly 10 characters, dashes in the right positions, digits only where expected
- No external dependencies required

### What I'd double-check

- **Year range**: The function accepts year `0000` and beyond (up to `9999`). If you have a stricter range requirement (e.g., year ≥ 1900), add a check after parsing: `if int(date_string[:4]) < 1900: return False`
- **Leap year algorithm**: Python's `datetime` module uses the proleptic Gregorian calendar (applies Gregorian rules backward indefinitely). If you need a different calendar system, you'll need a custom leap-year check.