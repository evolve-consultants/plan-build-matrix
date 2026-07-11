**Operating from: Bottom-Right (Build + Quality)**

### Confirming before I proceed

These are the key assumptions I'm acting on:
- You want a function that accepts a string and returns True/False (or raises on invalid input — I'll clarify in the code)
- "Strict ISO-8601" means YYYY-MM-DD format only; no time component, no timezone, no week dates, no ordinal dates
- "Real calendar dates" means it must reject invalid dates like 2024-02-30 and handle leap years correctly
- You own the verification — I'll list edge cases so you can test, but you'll validate against your actual requirements

<assumptions>
  <project>General-purpose validation function; no framework or existing codebase constraints implied</project>
  <task>You need a reliable date validator for input sanitization or data integrity checks</task>
  <operator>You're familiar with Python and will test this before deploying; you want to understand what it catches</operator>
</assumptions>

### The artifact

```python
from datetime import datetime

def is_valid_iso8601_date(date_string: str) -> bool:
    """
    Validate strict ISO-8601 date format (YYYY-MM-DD only).
    
    Returns True if the string represents a valid calendar date in that format.
    Returns False for any deviation from the format or invalid calendar dates.
    
    Args:
        date_string: String to validate
        
    Returns:
        bool: True if valid ISO-8601 date, False otherwise
    """
    # Check format: exactly 10 characters, dashes in right places
    if not isinstance(date_string, str) or len(date_string) != 10:
        return False
    
    if date_string[4] != '-' or date_string[7] != '-':
        return False
    
    # Check that year, month, day are all digits
    year_str, month_str, day_str = date_string.split('-')
    if not (year_str.isdigit() and month_str.isdigit() and day_str.isdigit()):
        return False
    
    # Convert to integers
    try:
        year = int(year_str)
        month = int(month_str)
        day = int(day_str)
    except ValueError:
        return False
    
    # Validate ranges: year positive, month 1-12
    if year < 1 or month < 1 or month > 12 or day < 1:
        return False
    
    # Use datetime to validate the actual calendar date
    # This catches Feb 30, Apr 31, invalid leap days, etc.
    try:
        datetime(year, month, day)
        return True
    except ValueError:
        return False
```

### Edge cases handled

| Edge Case | Example | Behavior |
|-----------|---------|----------|
| Valid date | `"2024-01-15"` | ✓ True |
| Leap year (valid) | `"2024-02-29"` | ✓ True |
| Leap year (invalid) | `"2023-02-29"` | ✗ False |
| Day out of range | `"2024-02-30"` | ✗ False |
| Month 31st violation | `"2024-04-31"` | ✗ False |
| Month = 0 | `"2024-00-15"` | ✗ False |
| Month = 13 | `"2024-13-01"` | ✗ False |
| Day = 0 | `"2024-01-00"` | ✗ False |
| Day = 32 | `"2024-01-32"` | ✗ False |
| Leading zeros (valid) | `"2024-01-05"` | ✓ True |
| Missing leading zeros | `"2024-1-5"` | ✗ False |
| Wrong separators | `"2024/01/15"` or `"2024.01.15"` | ✗ False |
| T instead of dash | `"2024T01-15"` | ✗ False |
| With time component | `"2024-01-15T10:30:00"` | ✗ False |
| With timezone | `"2024-01-15Z"` | ✗ False |
| Week date format | `"2024-W03-1"` | ✗ False |
| Ordinal date format | `"2024-015"` | ✗ False |
| Non-string input | `20240115` (int) or `None` | ✗ False |
| Empty string | `""` | ✗ False |
| Extra whitespace | `" 2024-01-15"` or `"2024-01-15 "` | ✗ False |
| Non-digit characters | `"202a-01-15"` | ✗ False |
| Year = 0 | `"0000-01-15"` | ✗ False |
| Negative year | Would fail digit check before range check | ✗ False |
| Very large year | `"9999-12-31"` | ✓ True |

### What I'm confident about
- The datetime constructor is the Python standard for calendar validation; it correctly handles all leap year rules and month lengths
- The format check is strict: wrong separators, wrong length, missing leading zeros all fail immediately
- Non-string inputs are caught by the `isinstance` check

### What I'd double-check
- **Year bounds**: The function allows year 1 and up, which is safe but you might want to add a max year check (e.g., `year <= 9999`) if you have application-specific constraints
- **Timezone/offset edge case**: If someone passes `"2024-01-15+00:00"`, it will fail (correct), but only after the length check. This is fine but worth knowing