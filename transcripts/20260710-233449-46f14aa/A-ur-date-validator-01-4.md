# Strict ISO-8601 Date Validator

```python
from datetime import datetime

def validate_iso8601_date(date_string: str) -> bool:
    """
    Validates strict ISO-8601 dates in YYYY-MM-DD format only.
    
    Args:
        date_string: The date string to validate
        
    Returns:
        True if valid ISO-8601 date (YYYY-MM-DD), False otherwise
    """
    # Check format: exactly 10 characters, hyphens in correct positions
    if not isinstance(date_string, str):
        return False
    
    if len(date_string) != 10:
        return False
    
    if date_string[4] != '-' or date_string[7] != '-':
        return False
    
    # Extract parts and validate they are numeric
    try:
        year_str, month_str, day_str = date_string.split('-')
    except ValueError:
        return False
    
    if not (year_str.isdigit() and month_str.isdigit() and day_str.isdigit()):
        return False
    
    # Convert to integers
    year = int(year_str)
    month = int(month_str)
    day = int(day_str)
    
    # Validate ranges
    if year < 1 or year > 9999:
        return False
    
    if month < 1 or month > 12:
        return False
    
    if day < 1:
        return False
    
    # Validate actual calendar date (handles leap years, month lengths)
    try:
        datetime(year, month, day)
        return True
    except ValueError:
        # Invalid date like Feb 30, April 31, etc.
        return False


# Test cases demonstrating edge cases handled
if __name__ == "__main__":
    test_cases = [
        # Valid dates
        ("2024-01-15", True, "Normal valid date"),
        ("2000-02-29", True, "Leap year (divisible by 400)"),
        ("2004-02-29", True, "Leap year (divisible by 4, not 100)"),
        ("1900-03-01", True, "NOT a leap year (divisible by 100, not 400)"),
        ("0001-01-01", True, "Minimum valid year"),
        ("9999-12-31", True, "Maximum valid year"),
        ("2024-12-31", True, "End of year"),
        ("2024-01-01", True, "Start of year"),
        
        # Invalid format
        ("2024/01/15", False, "Wrong separator (/)"),
        ("2024-1-15", False, "Single digit month without leading zero"),
        ("2024-01-5", False, "Single digit day without leading zero"),
        ("24-01-15", False, "Two-digit year"),
        ("2024-01-1", False, "Two-digit year, single-digit day"),
        ("20240115", False, "No separators"),
        ("2024-01-15T00:00:00", False, "Includes time component"),
        ("2024-01-15 ", False, "Trailing space"),
        (" 2024-01-15", False, "Leading space"),
        ("2024 -01-15", False, "Space in format"),
        
        # Invalid values
        ("2024-13-01", False, "Month > 12"),
        ("2024-00-01", False, "Month = 0"),
        ("2024-01-32", False, "Day > 31"),
        ("2024-01-00", False, "Day = 0"),
        ("2024-02-30", False, "February 30 (no such date)"),
        ("2023-02-29", False, "February 29 in non-leap year"),
        ("1900-02-29", False, "February 29 in 1900 (not a leap year)"),
        ("2100-02-29", False, "February 29 in 2100 (not a leap year)"),
        ("2024-04-31", False, "April 31 (April has 30 days)"),
        ("0000-01-01", False, "Year = 0"),
        ("10000-01-01", False, "Year > 9999"),
        
        # Wrong types
        (None, False, "None type"),
        (20240115, False, "Integer instead of string"),
        (2024.0115, False, "Float instead of string"),
        
        # Empty/whitespace
        ("", False, "Empty string"),
        ("          ", False, "Only spaces"),
        
        # Close but invalid
        ("2024-01-1a", False, "Non-numeric character"),
        ("202a-01-15", False, "Non-numeric character in year"),
        ("2024--01-15", False, "Double hyphen"),
        ("2024-01-15-", False, "Trailing hyphen"),
    ]
    
    print("ISO-8601 Date Validator Test Results\n" + "="*50)
    passed = 0
    failed = 0
    
    for date_str, expected, description in test_cases:
        result = validate_iso8601_date(date_str)
        status = "✓" if result == expected else "✗"
        
        if result == expected:
            passed += 1
        else:
            failed += 1
        
        print(f"{status} {description}")
        print(f"  Input: {repr(date_str)} → {result} (expected {expected})\n")
    
    print("="*50)
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
```

## Edge Cases Handled

### **Format Validation**
✓ Exact length (10 characters)  
✓ Hyphens in exact positions (indices 4 and 7)  
✓ Leading zeros required (no `2024-1-5`)  
✓ Rejects alternative separators (`/`, spaces, no separator)  
✓ Rejects time components  

### **Numeric Validation**
✓ All components must be digits  
✓ Rejects non-numeric characters  

### **Range Validation**
✓ Years: 1–9999 (rejects year 0 and 10000+)  
✓ Months: 1–12 (rejects 0 and 13+)  
✓ Days: 1–31 (rejects 0 and 32+)  

### **Calendar Reality** (via `datetime`)
✓ Leap years:
  - ✓ Year divisible by 400 → leap year (2000)
  - ✓ Year divisible by 100 (but not 400) → NOT leap year (1900, 2100)
  - ✓ Year divisible by 4 (but not 100) → leap year (2004)

✓ Month lengths (Feb 29, Apr 31, etc.)  
✓ February 29 validation for all years  

### **Type Safety**
✓ Rejects non-string inputs (None, int, float)  
✓ Handles empty strings  

### **Whitespace Handling**
✓ Rejects leading/trailing spaces  

Run the test suite to verify all edge cases! 🎯