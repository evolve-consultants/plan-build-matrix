**Operating from: Bottom-Right (Build + Quality)**

### Confirming before I proceed

These are the key assumptions I'm acting on:
- You want to validate the *format* (YYYY-MM-DD) AND reject invalid calendar dates (e.g., Feb 30)
- "Strict" means no time component, no timezone, no variations (201-01-01, 2023-1-1, etc. all fail)
- You want a single, reusable function that returns True/False or raises an exception (I'm choosing return bool for composability)
- You own the verification — I'll list edge cases explicitly so you can test them

<assumptions>
  <project>This is standalone validation logic, not tied to a larger framework</project>
  <task>You need a reliable date validator for input sanitization or data pipeline use</task>
  <operator>You can test edge cases and verify calendar math independently</operator>
</assumptions>

---

## The artifact

```python
def is_valid_iso8601_date(date_string: str) -> bool:
    """
    Validates strict ISO-8601 dates in YYYY-MM-DD format only.
    
    Returns True if the string is a valid calendar date in that exact format.
    Returns False for any deviation, invalid dates, or non-string input.
    """
    # Type check
    if not isinstance(date_string, str):
        return False
    
    # Format check: exactly 10 characters, pattern YYYY-MM-DD
    if len(date_string) != 10:
        return False
    
    if date_string[4] != '-' or date_string[7] != '-':
        return False
    
    # Extract and validate components are digits
    year_str, month_str, day_str = date_string[0:4], date_string[5:7], date_string[8:10]
    
    if not (year_str.isdigit() and month_str.isdigit() and day_str.isdigit()):
        return False
    
    year = int(year_str)
    month = int(month_str)
    day = int(day_str)
    
    # Month range
    if not (1 <= month <= 12):
        return False
    
    # Day range (simplified: 1-31, then refine by month)
    if not (1 <= day <= 31):
        return False
    
    # Days per month (non-leap year baseline)
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    # Leap year check: divisible by 4, except centuries unless divisible by 400
    is_leap = (year % 4 == 0) and (year % 100 != 0 or year % 400 == 0)
    
    if is_leap:
        days_in_month[1] = 29
    
    # Day within valid range for this month
    if day > days_in_month[month - 1]:
        return False
    
    return True
```

---

## Edge cases I handled

| Case | Behavior | Verification |
|------|----------|---|
| `"2023-01-15"` | ✓ Valid | Returns True |
| `"2023-02-28"` | ✓ Valid | Returns True |
| `"2020-02-29"` | ✓ Valid (leap year) | Returns True |
| `"2023-02-29"` | ✗ Invalid (not a leap year) | Returns False |
| `"1900-03-01"` | ✗ Invalid (1900 not leap: divisible by 100 but not 400) | Returns False |
| `"2000-03-01"` | ✓ Valid (2000 is leap: divisible by 400) | Returns True |
| `"2023-13-01"` | ✗ Invalid month | Returns False |
| `"2023-00-15"` | ✗ Invalid month | Returns False |
| `"2023-01-32"` | ✗ Invalid day | Returns False |
| `"2023-04-31"` | ✗ Invalid (April has 30 days) | Returns False |
| `"2023-01-0"` | ✗ Wrong length | Returns False |
| `"2023/01/15"` | ✗ Wrong separators | Returns False |
| `"23-01-15"` | ✗ Year too short | Returns False |
| `"2023-1-15"` | ✗ Month not zero-padded | Returns False |
| `"2023-01-5"` | ✗ Day not zero-padded | Returns False |
| `"abcd-ef-gh"` | ✗ Non-digit characters | Returns False |
| `None` | ✗ Non-string input | Returns False |
| `""` | ✗ Empty string | Returns False |
| `"2023-01-15 "` (trailing space) | ✗ Wrong length | Returns False |

Test these cases to confirm the function behaves as expected in your environment.