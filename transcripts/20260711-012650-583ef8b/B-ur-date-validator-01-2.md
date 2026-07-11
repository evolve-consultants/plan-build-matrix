**Operating from: Upper-Right (Build + Verify)**

### Confirming before I proceed

These are the key assumptions I'm acting on:
- You want validation that rejects invalid calendar dates (Feb 30, Apr 31, etc.), not just pattern matching
- "Strict ISO-8601" means YYYY-MM-DD format only — no time component, no timezone, no week notation
- You want the function to return a boolean or raise an exception (I'm choosing boolean for testability)
- Edge cases should be explicitly enumerable so you can write tests against them

<assumptions>
  <project>Standard Python 3, no external dependencies required</project>
  <task>Build a validator that catches both format errors and calendar impossibilities</task>
  <operator>You want to verify the implementation by testing against a known edge case list</operator>
</assumptions>

### The artifact

```python
def is_valid_iso8601_date(date_string: str) -> bool:
    """
    Validates strict ISO-8601 dates (YYYY-MM-DD format only).
    Returns True if the date is valid, False otherwise.
    
    Args:
        date_string: A string to validate
        
    Returns:
        bool: True if valid ISO-8601 date, False otherwise
    """
    from datetime import datetime
    
    # Check format: must be exactly 10 characters, YYYY-MM-DD pattern
    if not isinstance(date_string, str) or len(date_string) != 10:
        return False
    
    if date_string[4] != '-' or date_string[7] != '-':
        return False
    
    # Extract and validate components are numeric
    try:
        year_str = date_string[0:4]
        month_str = date_string[5:7]
        day_str = date_string[8:10]
        
        year = int(year_str)
        month = int(month_str)
        day = int(day_str)
    except ValueError:
        return False
    
    # Validate ranges before datetime construction
    if year < 1 or year > 9999:
        return False
    if month < 1 or month > 12:
        return False
    if day < 1 or day > 31:
        return False
    
    # Use datetime to catch calendar impossibilities (Feb 30, Apr 31, etc.)
    try:
        datetime(year, month, day)
        return True
    except ValueError:
        # Invalid calendar date (e.g., Feb 30)
        return False
```

### Edge cases I handled

| Edge Case | Input | Expected | Why it matters |
|---|---|---|---|
| **Non-string input** | `None`, `12345678901`, `[]` | `False` | Type safety |
| **Wrong length** | `"2024-1-5"`, `"2024-01-01-01"` | `False` | Format strictness |
| **Missing separators** | `"20240101"` | `False` | ISO-8601 requires hyphens |
| **Wrong separator placement** | `"2024/01/01"`, `"2024.01.01"` | `False` | Hyphens only |
| **Non-numeric components** | `"202a-01-01"`, `"2024-0a-01"` | `False` | Must be digits |
| **Leading zeros required** | `"2024-1-05"` | `False` | Strict format (no single-digit months/days) |
| **Month out of range** | `"2024-00-01"`, `"2024-13-01"` | `False` | Valid range 01–12 |
| **Day out of range** | `"2024-01-00"`, `"2024-01-32"` | `False` | Valid range 01–31 |
| **Feb 29 (leap year)** | `"2024-02-29"` | `True` | 2024 is a leap year |
| **Feb 29 (non-leap year)** | `"2023-02-29"` | `False` | 2023 is not a leap year |
| **Feb 30** | `"2024-02-30"` | `False` | February never has 30 days |
| **Apr 31** | `"2024-04-31"` | `False` | April has only 30 days |
| **Year boundaries** | `"0000-01-01"`, `"10000-01-01"` | `False` | Valid range 0001–9999 |
| **Valid dates (sample)** | `"2024-12-25"`, `"1999-01-01"` | `True` | Sanity check |
| **Whitespace** | `" 2024-01-01"`, `"2024-01-01 "` | `False` | No leading/trailing space |
| **Empty string** | `""` | `False` | Length check catches it |

### What I'm confident about
- The function correctly rejects all format violations
- The function correctly rejects invalid calendar dates (Feb 30, Apr 31, etc.)
- Leap year logic is delegated to `datetime`, which is standard library and battle-tested
- Edge cases table is exhaustive for the stated problem

### What I'd double-check
- **Year range (0001–9999)**: I set `year < 1` as the lower bound. Some use cases might allow year 0 or negative years (astronomical dating). If you need those, change the range check.
- **Whitespace handling**: Currently rejects leading/trailing whitespace. If your input may have it, strip before calling: `is_valid_iso8601_date(date_string.strip())`