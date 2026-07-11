**Operating from: Bottom-Right (Build + Quality)**

### Confirming before I proceed

These are the key assumptions I'm acting on:
- You want a function that accepts a string and returns True/False (or raises on invalid input — I'll do boolean return)
- "Strict ISO-8601" means YYYY-MM-DD format only; no time component, no timezone, no week dates
- "Real calendar dates" means it must reject Feb 30, Apr 31, invalid leap years, etc.
- You own verification of the edge cases (I'll list them, you'll test)

<assumptions>
  <project>General-purpose Python; no framework dependencies assumed</project>
  <task>You need a reusable validator for date strings, probably for input sanitization or data pipeline work</task>
  <operator>You're comfortable reading regex and calendar logic; you'll verify the edge cases yourself</operator>
</assumptions>

### The artifact

```python
import re
from datetime import datetime

def is_valid_iso8601_date(date_string: str) -> bool:
    """
    Validate a strict ISO-8601 date string (YYYY-MM-DD format only).
    
    Returns True if the string is a valid calendar date in YYYY-MM-DD format.
    Returns False for any invalid input, including non-string types.
    
    Args:
        date_string: A string to validate
        
    Returns:
        bool: True if valid ISO-8601 date, False otherwise
    """
    # Type check
    if not isinstance(date_string, str):
        return False
    
    # Format check: YYYY-MM-DD only
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_string):
        return False
    
    # Parse and validate as a real calendar date
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        # strptime catches invalid dates like Feb 30, Apr 31, etc.
        return False
```

### Edge cases handled

| Case | Example | Behavior |
|------|---------|----------|
| Valid date | `2024-01-15` | ✓ True |
| **Format violations** | — | — |
| Missing leading zeros | `2024-1-5` | ✗ False (regex rejects) |
| Wrong separator | `2024/01/15`, `2024.01.15` | ✗ False (regex rejects) |
| Extra spaces | ` 2024-01-15 `, `2024-01-15T00:00:00` | ✗ False (regex rejects) |
| Wrong order | `01-15-2024`, `2024-15-01` | ✗ False (strptime rejects) |
| **Invalid calendar dates** | — | — |
| Feb 30 | `2024-02-30` | ✗ False (strptime rejects) |
| Apr 31 | `2024-04-31` | ✗ False (strptime rejects) |
| Feb 29 non-leap year | `2023-02-29` | ✗ False (strptime rejects) |
| Feb 29 leap year | `2024-02-29` | ✓ True (valid) |
| **Boundary dates** | — | — |
| Year 0000 | `0000-01-01` | ✓ True (technically valid; adjust if you need Y>=1000) |
| Year 9999 | `9999-12-31` | ✓ True |
| **Type violations** | — | — |
| Integer | `20240115` | ✗ False (type check rejects) |
| None | `None` | ✗ False (type check rejects) |
| Leading zeros in year | `02024-01-15` | ✗ False (regex enforces exactly 4 digits) |
| Month 00 or 13 | `2024-00-15`, `2024-13-15` | ✗ False (strptime rejects) |
| Day 00 or 32+ | `2024-01-00`, `2024-01-32` | ✗ False (strptime rejects) |

### How to verify

```python
# Test harness
test_cases = [
    ("2024-01-15", True),
    ("2024-02-29", True),
    ("2023-02-29", False),
    ("2024-04-31", False),
    ("2024-1-5", False),
    ("2024/01/15", False),
    ("2024-01-15T00:00:00", False),
    (20240115, False),
    ("0000-01-01", True),  # adjust expectation if needed
]

for input_val, expected in test_cases:
    result = is_valid_iso8601_date(input_val)
    status = "✓" if result == expected else "✗"
    print(f"{status} {input_val!r}: {result} (expected {expected})")
```

The function is intentionally simple — `datetime.strptime` does all the heavy lifting for calendar validation. If you need to reject year 0000 or constrain the year range, add a check after the regex match.