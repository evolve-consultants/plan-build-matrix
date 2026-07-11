# Strict ISO-8601 Date Validator

```python
from datetime import datetime

def validate_iso8601_date(date_string):
    """
    Validates strict ISO-8601 dates in YYYY-MM-DD format.
    
    Args:
        date_string: String to validate
        
    Returns:
        dict: {
            'valid': bool,
            'error': str or None,
            'date': datetime.date or None
        }
    """
    if not isinstance(date_string, str):
        return {
            'valid': False,
            'error': 'Input must be a string',
            'date': None
        }
    
    # Check exact format (no extra whitespace, correct length)
    if len(date_string) != 10:
        return {
            'valid': False,
            'error': f'Invalid length: expected 10 characters, got {len(date_string)}',
            'date': None
        }
    
    # Check for exact format pattern
    if date_string[4] != '-' or date_string[7] != '-':
        return {
            'valid': False,
            'error': 'Invalid format: separators must be hyphens at positions 4 and 7',
            'date': None
        }
    
    year_str, month_str, day_str = date_string.split('-')
    
    # Verify all parts are numeric
    if not (year_str.isdigit() and month_str.isdigit() and day_str.isdigit()):
        return {
            'valid': False,
            'error': 'Year, month, and day must contain only digits',
            'date': None
        }
    
    # Check component lengths
    if len(year_str) != 4 or len(month_str) != 2 or len(day_str) != 2:
        return {
            'valid': False,
            'error': 'Invalid format: must be YYYY-MM-DD',
            'date': None
        }
    
    year = int(year_str)
    month = int(month_str)
    day = int(day_str)
    
    # Validate ranges before creating date object
    if month < 1 or month > 12:
        return {
            'valid': False,
            'error': f'Invalid month: {month} (must be 01-12)',
            'date': None
        }
    
    if day < 1 or day > 31:
        return {
            'valid': False,
            'error': f'Invalid day: {day} (must be 01-31)',
            'date': None
        }
    
    # Try to create a real calendar date (validates leap years, month lengths, etc.)
    try:
        date_obj = datetime.strptime(date_string, '%Y-%m-%d').date()
        return {
            'valid': True,
            'error': None,
            'date': date_obj
        }
    except ValueError as e:
        return {
            'valid': False,
            'error': f'Invalid calendar date: {str(e)}',
            'date': None
        }


# Test cases demonstrating edge cases
if __name__ == '__main__':
    test_cases = [
        # Valid dates
        ('2024-01-15', True, 'Standard valid date'),
        ('2000-02-29', True, 'Leap year (divisible by 400)'),
        ('2004-02-29', True, 'Leap year (divisible by 4, not 100)'),
        ('1999-12-31', True, 'End of year'),
        ('2000-01-01', True, 'Start of millennium'),
        
        # Invalid format
        ('2024-1-15', False, 'Single digit month (missing leading zero)'),
        ('2024-01-5', False, 'Single digit day (missing leading zero)'),
        ('2024/01/15', False, 'Wrong separator (slash instead of hyphen)'),
        ('2024.01.15', False, 'Wrong separator (dot instead of hyphen)'),
        ('24-01-15', False, 'Two-digit year'),
        ('2024-01-15 ', False, 'Trailing whitespace'),
        (' 2024-01-15', False, 'Leading whitespace'),
        ('2024-01-1', False, 'Incomplete (9 chars)'),
        ('2024-01-155', False, 'Too long (11 chars)'),
        ('2024-013-15', False, 'Month not zero-padded'),
        
        # Invalid calendar dates
        ('2024-02-30', False, 'February 30th (invalid day for month)'),
        ('2023-02-29', False, 'Feb 29 in non-leap year'),
        ('1900-02-29', False, 'Leap year rule: 1900 divisible by 100 but not 400'),
        ('2024-04-31', False, 'April 31st (April has 30 days)'),
        ('2024-13-01', False, 'Month 13 (out of range)'),
        ('2024-00-15', False, 'Month 00 (out of range)'),
        ('2024-01-00', False, 'Day 00 (out of range)'),
        ('2024-01-32', False, 'Day 32 (out of range)'),
        
        # Non-string inputs
        (20240115, False, 'Integer instead of string'),
        (None, False, 'None value'),
        ([], False, 'List instead of string'),
        
        # Ambiguous/tricky cases
        ('2024-01-15T00:00:00', False, 'ISO-8601 datetime (not just date)'),
        ('2024-01-15Z', False, 'ISO-8601 with timezone'),
        ('2024-01-15\n', False, 'Newline character'),
        ('2024-01-15\t', False, 'Tab character'),
        ('2024-01-1a', False, 'Non-numeric character in day'),
    ]
    
    print("VALIDATION TEST RESULTS\n" + "="*70)
    
    for date_str, expected_valid, description in test_cases:
        result = validate_iso8601_date(date_str)
        status = '✓ PASS' if result['valid'] == expected_valid else '✗ FAIL'
        
        print(f"\n{status} | {description}")
        print(f"  Input: {repr(date_str)}")
        print(f"  Result: {'VALID' if result['valid'] else 'INVALID'}")
        if result['error']:
            print(f"  Error: {result['error']}")
        if result['date']:
            print(f"  Date: {result['date']}")
```

## Edge Cases Handled ✓

### **Format Validation**
- ✓ Exact length (10 characters only)
- ✓ Hyphen positions (must be at indices 4 and 7)
- ✓ Numeric-only components
- ✓ Zero-padded month and day (MM and DD required)
- ✓ Four-digit year

### **Calendar Validation**
- ✓ Month range (01-12)
- ✓ Day range (01-31 base, then calendar-aware)
- ✓ Leap years (400-divisible, 4-divisible but not 100)
- ✓ Month-specific day counts (February 28/29, April 30, etc.)

### **Type Safety**
- ✓ Non-string inputs rejected
- ✓ None values handled
- ✓ Empty strings handled

### **Strict ISO-8601**
- ✓ Rejects datetime format (with time component)
- ✓ Rejects timezone indicators (Z, ±HH:MM)
- ✓ Rejects whitespace (leading, trailing, embedded)
- ✓ Rejects other separators (/, ., space)

The function returns detailed error messages so you can diagnose why validation failed!