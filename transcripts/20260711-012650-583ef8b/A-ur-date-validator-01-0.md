# Strict ISO-8601 Date Validator

```python
from datetime import datetime

def validate_iso8601_date(date_string: str) -> bool:
    """
    Validates strict ISO-8601 dates in YYYY-MM-DD format.
    
    Args:
        date_string: String to validate
        
    Returns:
        True if valid ISO-8601 date, False otherwise
    """
    # Check type
    if not isinstance(date_string, str):
        return False
    
    # Check exact format and length
    if len(date_string) != 10:
        return False
    
    # Check format: YYYY-MM-DD
    if date_string[4] != '-' or date_string[7] != '-':
        return False
    
    # Extract and validate components
    try:
        year_str, month_str, day_str = date_string.split('-')
        
        # Verify all parts are numeric
        if not (year_str.isdigit() and month_str.isdigit() and day_str.isdigit()):
            return False
        
        year = int(year_str)
        month = int(month_str)
        day = int(day_str)
        
        # Validate ranges before datetime creation
        if year < 1 or year > 9999:
            return False
        
        if month < 1 or month > 12:
            return False
        
        if day < 1:
            return False
        
        # This validates calendar legitimacy (leap years, month lengths, etc.)
        datetime(year, month, day)
        return True
        
    except (ValueError, IndexError):
        return False


# Test cases with edge cases documented
test_cases = [
    # Valid dates
    ("2024-01-15", True, "Standard valid date"),
    ("2000-02-29", True, "Leap year (divisible by 400)"),
    ("2004-02-29", True, "Leap year (divisible by 4, not 100)"),
    ("1900-01-01", True, "Not a leap year (divisible by 100, not 400)"),
    ("0001-01-01", True, "Minimum year (year 1)"),
    ("9999-12-31", True, "Maximum year (year 9999)"),
    ("2024-12-31", True, "Last day of year"),
    ("2024-01-01", True, "First day of year"),
    
    # Invalid formats
    ("2024-1-15", False, "Missing leading zero in month"),
    ("2024-01-5", False, "Missing leading zero in day"),
    ("24-01-15", False, "Two-digit year"),
    ("2024/01/15", False, "Wrong separator (slash)"),
    ("2024.01.15", False, "Wrong separator (dot)"),
    ("20240115", False, "No separators"),
    ("2024-01-15T10:30:00", False, "Includes time component"),
    ("2024-01-15 ", False, "Trailing whitespace"),
    (" 2024-01-15", False, "Leading whitespace"),
    ("", False, "Empty string"),
    ("2024-13-01", False, "Invalid month (13)"),
    ("2024-00-15", False, "Invalid month (0)"),
    ("2024-01-32", False, "Invalid day (32)"),
    ("2024-01-00", False, "Invalid day (0)"),
    ("2024-02-30", False, "Feb 30th (doesn't exist)"),
    ("2024-04-31", False, "April 31st (April has 30 days)"),
    ("1900-02-29", False, "1900 not a leap year (divisible by 100, not 400)"),
    ("2100-02-29", False, "2100 not a leap year (divisible by 100, not 400)"),
    ("2024-02-29", True, "2024 is leap year"),
    ("2023-02-29", False, "2023 not leap year"),
    ("0000-01-01", False, "Year 0 (invalid, min is 1)"),
    ("10000-01-01", False, "Year 10000 (exceeds max)"),
    ("-2024-01-15", False, "Negative year"),
    ("2024-01-15-01", False, "Extra hyphen"),
    ("2024-01", False, "Incomplete date"),
    ("2024-01-", False, "Incomplete date"),
    ("-01-15", False, "Missing year"),
    ("2024-ab-15", False, "Non-numeric month"),
    ("2024-01-ab", False, "Non-numeric day"),
    ("2024-01-15.0", False, "Decimal portion"),
    (123, False, "Non-string input (integer)"),
    (None, False, "None input"),
    (["2024-01-15"], False, "List input"),
]

# Run tests
print("=" * 70)
print("ISO-8601 DATE VALIDATOR - TEST RESULTS")
print("=" * 70)

passed = 0
failed = 0

for test_input, expected, description in test_cases:
    result = validate_iso8601_date(test_input)
    status = "✓ PASS" if result == expected else "✗ FAIL"
    
    if result == expected:
        passed += 1
    else:
        failed += 1
    
    print(f"{status} | {str(test_input):25} | Expected: {str(expected):5} | {description}")

print("=" * 70)
print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
print("=" * 70)
```

## Edge Cases Handled

### **Format Validation**
- ✓ Exact length check (10 characters)
- ✓ Hyphens at correct positions (indices 4 and 7)
- ✓ No leading/trailing whitespace
- ✓ Rejects time components
- ✓ No alternative separators (/, ., etc.)

### **Numeric Validation**
- ✓ All components must be digits
- ✓ Leading zeros required
- ✓ Two-digit years rejected
- ✓ Non-string inputs rejected

### **Calendar Validation**
- ✓ Month range: 1-12
- ✓ Day range: 1-31 (based on month)
- ✓ **Leap year logic:**
  - Years divisible by 400 are leap years (2000 ✓)
  - Years divisible by 100 are NOT leap years (1900, 2100 ✗)
  - Years divisible by 4 are leap years (2004 ✓)
  - Other years are not leap years
- ✓ Month lengths: 30/31-day validation
- ✓ Feb 29 only in leap years

### **Range Validation**
- ✓ Year: 1-9999 (ISO-8601 standard)
- ✓ Year 0 rejected (invalid calendar)
- ✓ Negative years rejected
- ✓ Year 10000+ rejected

The function uses Python's `datetime` constructor as a final validation gate, ensuring real calendar dates only.