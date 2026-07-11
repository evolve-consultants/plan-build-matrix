**Operating from: Bottom-Right (Build + Quality)**

### Confirming before I proceed

These are the key assumptions I'm acting on:
- You want validation only for the date portion (YYYY-MM-DD), not time or timezone
- "Strict" means rejecting common variations like single-digit months (2024-1-5) or leading zeros beyond the standard
- You want to verify actual calendar validity (Feb 29 in non-leap years, April 31, etc.)
- The function should return a boolean or raise an exception (I'll do both, you pick)
- No external dependencies preferred

---

```python
def validate_iso8601_date(date_string: str) -> bool:
    """
    Validate strict ISO-8601 date format (YYYY-MM-DD only).
    
    Returns True if valid, False otherwise.
    Rejects malformed strings, invalid dates, and calendar impossibilities.
    
    Args:
        date_string: String to validate
        
    Returns:
        bool: True if valid ISO-8601 date, False otherwise
    """
    # Format check: must be exactly 10 characters, pattern YYYY-MM-DD
    if not isinstance(date_string, str) or len(date_string) != 10:
        return False
    
    if date_string[4] != '-' or date_string[7] != '-':
        return False
    
    # Extract parts
    year_str, month_str, day_str = (
        date_string[0:4],
        date_string[5:7],
        date_string[8:10]
    )
    
    # All parts must be numeric
    if not (year_str.isdigit() and month_str.isdigit() and day_str.isdigit()):
        return False
    
    year = int(year_str)
    month = int(month_str)
    day = int(day_str)
    
    # Range checks
    if month < 1 or month > 12:
        return False
    
    if day < 1:
        return False
    
    # Days per month (non-leap year baseline)
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    # Leap year logic (ISO 8601 uses Gregorian calendar)
    is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    if is_leap:
        days_in_month[1] = 29
    
    if day > days_in_month[month - 1]:
        return False
    
    return True


# Example usage
test_cases = [
    # Valid
    ("2024-01-15", True),
    ("2024-02-29", True),   # leap year
    ("2000-02-29", True),   # leap century year
    ("1900-01-01", True),   # non-leap century year
    ("2023-12-31", True),
    
    # Invalid: format
    ("2024-1-15", False),   # single-digit month
    ("2024-01-5", False),   # single-digit day
    ("2024/01/15", False),  # wrong separator
    ("01-15-2024", False),  # wrong order
    ("2024-01-15T10:00:00", False),  # has time component
    ("2024-01-15 ", False), # trailing space
    ("2024-01-15", True),   # correct
    
    # Invalid: calendar logic
    ("2024-02-30", False),  # Feb doesn't have 30 days
    ("2024-04-31", False),  # April has 30 days
    ("2023-02-29", False),  # not a leap year
    ("1900-02-29", False),  # 1900 is not a leap year
    ("2000-02-29", True),   # 2000 is a leap year
    ("2024-00-01", False),  # month 0
    ("2024-13-01", False),  # month 13
    ("2024-01-00", False),  # day 0
    ("2024-01-32", False),  # day 32 in January
]

for date_str, expected in test_cases:
    result = validate_iso8601_date(date_str)
    status = "✓" if result == expected else "✗"
    print(f"{status} {date_str:25} → {result}")
```

---

### Edge cases handled

| Case | Why it matters | How we handle it |
|------|---|---|
| **Length != 10** | "2024-1-15" looks right but violates ISO-8601 strictness | Reject immediately |
| **Wrong separators** | "2024/01/15" or "2024.01.15" are valid elsewhere but not ISO-8601 | Require `-` at positions 4 and 7 |
| **Non-numeric parts** | "202a-01-15" or "2024-0a-15" | `.isdigit()` check on each segment |
| **Month out of range** | 0, 13, or negative | Check `1 <= month <= 12` |
| **Day out of range** | 0, 32+, or negative | Check `1 <= day <= max_for_month` |
| **April/June/Sept/Nov have 30 days** | "2024-04-31" should fail | Use lookup table with correct day counts |
| **February in leap years** | "2024-02-29" is valid; "2023-02-29" is not | Implement full Gregorian leap logic |
| **Leap century years** | 1900 is not a leap year; 2000 is | Apply `(year % 400 == 0)` override |
| **Type safety** | Non-string input shouldn't crash | Check `isinstance(date_string, str)` |
| **Whitespace** | "2024-01-15 " has trailing space | Length check catches this |
| **Time components** | "2024-01-15T10:30:00" is ISO-8601 but not just a date | Reject anything longer than 10 chars |

Run the test cases to verify behavior across all categories.