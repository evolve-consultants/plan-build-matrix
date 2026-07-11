# Strict ISO-8601 Date Validator

```python
from datetime import datetime

def validate_iso8601_date(date_string: str) -> bool:
    """
    Validates strict ISO-8601 dates in YYYY-MM-DD format only.
    
    Args:
        date_string: String to validate
        
    Returns:
        True if valid ISO-8601 date, False otherwise
    """
    # Check if None or not a string
    if not isinstance(date_string, str):
        return False
    
    # Check exact format (12 chars with hyphens at positions 4 and 7)
    if len(date_string) != 10:
        return False
    
    if date_string[4] != '-' or date_string[7] != '-':
        return False
    
    # Extract parts and validate they're digits
    year_str, month_str, day_str = date_string.split('-')
    
    if not (year_str.isdigit() and month_str.isdigit() and day_str.isdigit()):
        return False
    
    # Check length of components
    if len(year_str) != 4 or len(month_str) != 2 or len(day_str) != 2:
        return False
    
    year = int(year_str)
    month = int(month_str)
    day = int(day_str)
    
    # Validate month range
    if month < 1 or month > 12:
        return False
    
    # Validate day range using datetime (handles leap years automatically)
    try:
        datetime(year, month, day)
        return True
    except ValueError:
        # Invalid day for the given month/year (e.g., Feb 30)
        return False


# Test cases demonstrating edge cases handled
if __name__ == "__main__":
    test_cases = [
        # Valid dates
        ("2024-01-15", True, "Standard valid date"),
        ("2000-02-29", True, "Leap year (divisible by 400)"),
        ("2024-02-29", True, "Leap year (divisible by 4, not 100)"),
        ("1900-03-15", True, "Year 1900 (not a leap year)"),
        ("9999-12-31", True, "Max year"),
        ("0001-01-01", True, "Min year"),
        
        # Invalid dates - format issues
        ("2024-1-15", False, "Month without leading zero"),
        ("2024-01-5", False, "Day without leading zero"),
        ("2024/01/15", False, "Wrong separator (slashes)"),
        ("2024.01.15", False, "Wrong separator (dots)"),
        ("20240115", False, "No separators"),
        ("2024-01-15T00:00:00", False, "Includes time component"),
        ("2024-01-15 ", False, "Trailing space"),
        (" 2024-01-15", False, "Leading space"),
        ("2024-01-1", False, "Missing leading zero on day"),
        ("2024-01-15-01", False, "Extra component"),
        ("24-01-15", False, "2-digit year"),
        ("02024-01-15", False, "5-digit year"),
        
        # Invalid dates - value issues
        ("2024-13-01", False, "Month 13"),
        ("2024-00-01", False, "Month 0"),
        ("2024-01-32", False, "Day 32 in January"),
        ("2024-02-30", False, "Feb 30 (non-leap year)"),
        ("2023-02-29", False, "Feb 29 in non-leap year"),
        ("1900-02-29", False, "Leap year exception (1900)"),
        ("2024-04-31", False, "Day 31 in April (only 30 days)"),
        ("2024-06-31", False, "Day 31 in June (only 30 days)"),
        
        # Invalid types
        (None, False, "None value"),
        (20240115, False, "Integer instead of string"),
        (2024.0115, False, "Float"),
        ([], False, "List"),
        ({}, False, "Dictionary"),
        
        # Empty/whitespace
        ("", False, "Empty string"),
        ("          ", False, "Only spaces"),
        
        # Edge cases - characters
        ("202a-01-15", False, "Letter in year"),
        ("2024-0a-15", False, "Letter in month"),
        ("2024-01-1a", False, "Letter in day"),
        ("2024-01-15\n", False, "Newline at end"),
        ("2024--01-15", False, "Double hyphen"),
        ("2024-01--15", False, "Double hyphen between day"),
    ]
    
    passed = 0
    failed = 0
    
    for date_str, expected, description in test_cases:
        result = validate_iso8601_date(date_str)
        status = "✓" if result == expected else "✗"
        
        if result == expected:
            passed += 1
        else:
            failed += 1
            
        print(f"{status} {description:40} | Input: {str(date_str):25} | "
              f"Expected: {expected:5} | Got: {result:5}")
    
    print(f"\n{'='*100}")
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
```

## Edge Cases Handled

| Category | Edge Cases |
|----------|-----------|
| **Format** | Wrong separators (/, .), missing separators, extra components, incorrect component length |
| **Components** | Single-digit month/day without leading zeros, wrong number of digits in year |
| **Month/Day Values** | Month 0, Month 13+, Day 32+, invalid days per month (e.g., Feb 30, Apr 31) |
| **Leap Years** | Feb 29 on leap years (divisible by 4 but not 100, OR divisible by 400), Feb 29 on non-leap years, special case 1900 |
| **Type Validation** | None, integers, floats, lists, dicts, other non-string types |
| **Whitespace** | Leading/trailing spaces, newlines, tab characters |
| **Time Components** | Rejection of ISO-8601 with time (T00:00:00), timezone info |
| **Edge Years** | Very small years (0001), very large years (9999) |

The function uses Python's `datetime` constructor to validate real calendar dates, which automatically handles leap year logic and month lengths.