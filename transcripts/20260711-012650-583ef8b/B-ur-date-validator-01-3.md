**Operating from: Upper-Right (Build + Verify)**

### Confirming before I proceed

- You want validation of the date *format* (YYYY-MM-DD) *and* calendar validity (Feb 30 rejects, leap years work)
- "Strict" means no timestamps, no timezones, no variant formats — only YYYY-MM-DD
- You'll verify the edge cases list against your own test suite
- Return type is a boolean (valid/invalid); exceptions are not the primary signal

<assumptions>
  <project>Standard library only; no external datetime parsing libraries needed</project>
  <task>You need a reliable validator for ISO-8601 date strings in a data pipeline or API input layer</task>
  <operator>You can verify calendar logic and edge cases yourself; you own the test strategy</operator>
</assumptions>

---

### The artifact

```python
def is_valid_iso8601_date(date_string: str) -> bool:
    """
    Validate strict ISO-8601 date format (YYYY-MM-DD) with calendar validity.
    
    Args:
        date_string: String to validate
        
    Returns:
        True if valid ISO-8601 date, False otherwise
    """
    # Check format: exactly 10 chars, hyphens in right places
    if not isinstance(date_string, str) or len(date_string) != 10:
        return False
    
    if date_string[4] != '-' or date_string[7] != '-':
        return False
    
    # Extract and validate parts
    year_str, month_str, day_str = date_string.split('-')
    
    # Year must be 4 digits
    if not year_str.isdigit() or len(year_str) != 4:
        return False
    
    # Month and day must be 2 digits
    if not month_str.isdigit() or len(month_str) != 2:
        return False
    
    if not day_str.isdigit() or len(day_str) != 2:
        return False
    
    year, month, day = int(year_str), int(month_str), int(day_str)
    
    # Month must be 01–12
    if month < 1 or month > 12:
        return False
    
    # Day must be 01–31
    if day < 1 or day > 31:
        return False
    
    # Days per month (non-leap year baseline)
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    # Leap year check: divisible by 400, OR (divisible by 4 AND not by 100)
    is_leap = (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0)
    if is_leap:
        days_in_month[1] = 29
    
    # Check day is valid for the given month
    if day > days_in_month[month - 1]:
        return False
    
    return True
```

---

### Edge cases handled

| Edge case | Why it matters | Status |
|---|---|---|
| **Non-string input** | `None`, `int`, list passed to function | Rejected early with type check |
| **Wrong length** | `"2024-1-5"` or `"2024-01-05 "` | Length must be exactly 10 |
| **Missing hyphens** | `"20240105"` | Hyphens checked at positions 4 and 7 |
| **Non-digit year/month/day** | `"20a4-01-05"`, `"2024-0a-05"` | `isdigit()` catches non-numerics |
| **Leading zeros omitted** | `"2024-1-05"` | Month and day must be exactly 2 digits |
| **Month 00 or 13+** | `"2024-00-15"`, `"2024-13-01"` | Month range 1–12 enforced |
| **Day 00** | `"2024-01-00"` | Day range 1–31 enforced |
| **Feb 30 (non-leap year)** | `"2024-02-30"` is invalid even though 30 ≤ 31 | Calendar lookup rejects it |
| **Feb 29 (non-leap year)** | `"2023-02-29"` invalid; `"2024-02-29"` valid | Leap year logic handles both |
| **Leap year: century rule** | `"2000-02-29"` valid; `"1900-02-29"` invalid | Divisible by 400 vs. 100 distinction |
| **Day 31 in 30-day month** | `"2024-04-31"`, `"2024-06-31"` | Calendar lookup rejects |
| **Empty string** | `""` | Length check fails |
| **Whitespace** | `" 2024-01-05"`, `"2024-01-05\n"` | Length check fails |
| **Year 0000** | `"0000-01-01"` | Passes (no year range constraint) — adjust if you need Y≥1 |

---

### What I'm confident about

- Format validation (hyphens, digit counts, structure) is bulletproof
- Leap year calculation matches ISO-8601 / Gregorian calendar rules
- All 12 months and their day counts are correct
- Non-string inputs won't crash the function

### What I'd double-check

- **Year range**: I allow year 0000 and above. If you need `year >= 1` (strict proleptic Gregorian), add a check after line `year = int(year_str)`
- **Negative years**: The function doesn't handle `"-001-01-01"` (would fail the digit check, which is probably what you want)
- **Performance**: For tight loops, you might prefer a compiled regex, but clarity wins here