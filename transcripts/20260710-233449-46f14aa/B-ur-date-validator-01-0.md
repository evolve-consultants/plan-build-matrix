**Operating from: Bottom-Right (Build + Quality)**

### Confirming before I proceed

These are the key assumptions I'm acting on:

- You want a function that accepts a string and returns `True`/`False` (or raises an exception — I'll go with return values)
- "Strict ISO-8601" means `YYYY-MM-DD` format exactly; no time component, no timezone, no week dates
- "Real calendar dates" means it should reject Feb 30, Nov 31, invalid leap years, etc.
- You own the factual verification of edge cases (I'll list them so you can spot-check the logic)

<assumptions>
  <project>Pure Python, no external dependencies assumed</project>
  <task>You need a reusable validator, likely for input sanitization or data pipeline work</task>
  <operator>You can read code and verify logic yourself; you want transparency on what's being checked</operator>
</assumptions>

---

```python
def is_valid_iso8601_date(date_string: str) -> bool:
    """
    Validate strict ISO-8601 date format (YYYY-MM-DD only).
    
    Returns True if the string is a valid calendar date in YYYY-MM-DD format.
    Returns False for any deviation or invalid date.
    
    Args:
        date_string: The string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Check format: exactly 10 characters, correct positions of hyphens
    if len(date_string) != 10:
        return False
    
    if date_string[4] != '-' or date_string[7] != '-':
        return False
    
    # Extract and validate components are numeric
    year_str, month_str, day_str = date_string[:4], date_string[5:7], date_string[8:10]
    
    if not (year_str.isdigit() and month_str.isdigit() and day_str.isdigit()):
        return False
    
    year, month, day = int(year_str), int(month_str), int(day_str)
    
    # Validate ranges
    if not (1 <= month <= 12):
        return False
    
    if not (1 <= day <= 31):
        return False
    
    # Days per month (non-leap)
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    # Leap year logic: divisible by 4, except centuries (divisible by 100) 
    # unless also divisible by 400
    is_leap = (year % 4 == 0) and (year % 100 != 0 or year % 400 == 0)
    
    if is_leap:
        days_in_month[1] = 29
    
    # Validate day against the month
    if day > days_in_month[month - 1]:
        return False
    
    return True
```

---

### Edge cases handled

| Edge Case | Example | Handled By |
|---|---|---|
| Wrong length | `"2024-1-5"` or `"2024-01-05x"` | Length check (must be 10) |
| Missing hyphens | `"20240105"` | Hyphen position validation |
| Wrong hyphen positions | `"2024/01/05"` | Explicit check on positions 4 and 7 |
| Non-numeric characters | `"202a-01-05"` or `"2024-0a-05"` | `isdigit()` check on all three components |
| Invalid month | `"2024-13-05"` or `"2024-00-05"` | Month range check (1–12) |
| Invalid day (high) | `"2024-01-32"` | Day range check (1–31) and month-specific max |
| Invalid day (low) | `"2024-01-00"` | Day range check (≥1) |
| February 29 on non-leap year | `"2023-02-29"` | Leap year logic + days-in-month lookup |
| February 28 on leap year | `"2024-02-28"` | Accepted (always valid) |
| February 29 on leap year | `"2024-02-29"` | Accepted (leap year detected) |
| Century non-leap | `"1900-02-29"` | Leap logic: 1900 % 100 = 0 and % 400 ≠ 0 → not leap |
| Century leap | `"2000-02-29"` | Leap logic: 2000 % 400 = 0 → leap |
| 30-day months | `"2024-04-31"` or `"2024-06-31"` | Days-in-month lookup |
| Year 0000 | `"0000-01-01"` | Accepted (no year range constraint; adjust if needed) |
| Negative year | `"-100-01-01"` | Rejected (hyphen in position 4, not position 0) |
| Leading zeros | `"2024-01-05"` | Accepted (ISO-8601 standard) |
| Leap year cycle (4, 100, 400) | `2004, 2100, 2000` | All covered by the three-part leap check |

---

You can verify the leap year logic by testing the boundary years: 1900, 2000, 2004, 2100.