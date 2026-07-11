**Operating from: Bottom-Right (Build + Quality)**

### Confirming before I proceed
- You want validation only for the `YYYY-MM-DD` format (no time, timezone, or week notation)
- "Strict" means rejecting invalid calendar dates (e.g., Feb 30, month 13)
- You own factual verification and will check the edge cases list
- Return value should be boolean (valid/invalid)

<assumptions>
  <project>Standard Python 3.6+, no external dependencies required</project>
  <task>A reusable, single-purpose validator for ISO-8601 date strings with clear edge case handling</task>
  <operator>You can verify the logic against a calendar and will test edge cases yourself</operator>
</assumptions>

---

```python
def is_valid_iso8601_date(date_string: str) -> bool:
    """
    Validates strict ISO-8601 dates in YYYY-MM-DD format.
    Returns True only for real calendar dates; False otherwise.
    """
    # Format check: must be exactly 10 characters, pattern YYYY-MM-DD
    if not isinstance(date_string, str) or len(date_string) != 10:
        return False
    
    if date_string[4] != '-' or date_string[7] != '-':
        return False
    
    # Extract and validate year, month, day are digits
    try:
        year_str, month_str, day_str = (
            date_string[0:4],
            date_string[5:7],
            date_string[8:10]
        )
        
        if not (year_str.isdigit() and month_str.isdigit() and day_str.isdigit()):
            return False
        
        year = int(year_str)
        month = int(month_str)
        day = int(day_str)
    except (ValueError, IndexError):
        return False
    
    # Month must be 01–12
    if month < 1 or month > 12:
        return False
    
    # Day must be 01–31 at minimum
    if day < 1 or day > 31:
        return False
    
    # Days-per-month with leap year logic
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    # Leap year: divisible by 4, except centuries (divisible by 100)
    # unless also divisible by 400
    is_leap = (year % 4 == 0) and (year % 100 != 0 or year % 400 == 0)
    if is_leap:
        days_in_month[1] = 29
    
    # Day must not exceed the actual number of days in that month
    if day > days_in_month[month - 1]:
        return False
    
    return True
```

---

### Edge cases handled

| Case | Example | Behavior |
|------|---------|----------|
| **Wrong type** | `None`, `123`, `[]` | Rejects (not a string) |
| **Wrong length** | `"2024-1-5"`, `"2024-01-05x"` | Rejects (not exactly 10 chars) |
| **Wrong separators** | `"2024/01/05"`, `"2024.01.05"` | Rejects (hyphens required) |
| **Non-digit characters** | `"202a-01-05"`, `"2024-0a-05"` | Rejects (non-digits in Y/M/D) |
| **Month = 0** | `"2024-00-05"` | Rejects (month < 1) |
| **Month = 13** | `"2024-13-05"` | Rejects (month > 12) |
| **Day = 0** | `"2024-01-00"` | Rejects (day < 1) |
| **Day = 32** | `"2024-01-32"` | Rejects (day > 31) |
| **Feb 29 (non-leap)** | `"2023-02-29"` | Rejects (Feb has 28 days) |
| **Feb 29 (leap year)** | `"2024-02-29"` | Accepts (leap year) |
| **Feb 30 (all years)** | `"2024-02-30"` | Rejects (Feb max 29) |
| **Apr 31** | `"2024-04-31"` | Rejects (Apr has 30 days) |
| **Valid date** | `"2024-01-15"` | Accepts |
| **Year 0000** | `"0000-01-01"` | Accepts (no year bounds enforced) |
| **Year 9999** | `"9999-12-31"` | Accepts (no year bounds enforced) |
| **Leading zeros required** | `"2024-1-05"` | Rejects (month must be 2-digit) |

**Note:** This function accepts any 4-digit year (0000–9999) with no range validation. If you need to reject years before a certain epoch, add a year bounds check after the leap-year logic.