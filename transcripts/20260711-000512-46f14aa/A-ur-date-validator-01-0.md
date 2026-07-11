Here's a strict ISO-8601 date validator:

```python
import re
from datetime import date

# Exactly 4 digits - 2 digits - 2 digits, ASCII digits only, no extra chars
_ISO_DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$', re.ASCII)

def is_valid_iso_date(s: str) -> bool:
    """
    Validate that `s` is a strict ISO-8601 calendar date in YYYY-MM-DD form,
    representing a real calendar date.
    """
    if not isinstance(s, str):
        return False

    if not _ISO_DATE_RE.fullmatch(s):
        return False

    year_str, month_str, day_str = s.split('-')
    year, month, day = int(year_str), int(month_str), int(day_str)

    try:
        date(year, month, day)
    except ValueError:
        return False

    return True
```

### Edge cases handled

**Format-level (regex + `re.ASCII`):**
- Non-string input (`None`, `int`, `date` objects, etc.) → rejected before regex
- Wrong separators (`2024/01/01`, `2024.01.01`) → rejected
- Missing zero-padding (`2024-1-5`) → rejected (must be exactly 2 digits for month/day)
- Wrong digit counts (`24-01-01`, `2024-001-01`) → rejected
- Leading/trailing whitespace or extra characters (`" 2024-01-01"`, `"2024-01-01x"`) → rejected via `fullmatch`
- Alternate ISO forms not allowed by "YYYY-MM-DD only": basic format without dashes (`20240101`), ordinal dates (`2024-032`), week dates (`2024-W05-3`), datetime with time component (`2024-01-01T00:00:00`)
- Unicode "fake" digits (e.g., full-width `２０２４-０１-０１`) → rejected because `re.ASCII` restricts `\d` to `0–9`
- Negative years / expanded year format (`-0001-01-01`, `+02024-01-01`) → rejected, since only exactly 4 plain digits are allowed

**Calendar-level (via `datetime.date`):**
- Month out of range: `00`, `13+`
- Day out of range: `00`, `32+`
- Day invalid for specific month (e.g., `2024-04-31`, `2024-06-31`)
- February in non-leap year: `2023-02-29` → invalid
- February in leap year: `2024-02-29` → valid
- Century-year leap rule: `1900-02-29` → invalid (divisible by 100, not 400), `2000-02-29` → valid (divisible by 400)
- Year `0000` → invalid, since Python's `date` requires `MINYEAR = 1` (there's no astronomical year-zero support here)
- Upper bound: years above `9999` are already excluded by the 4-digit regex; `9999-12-31` is the max valid date

### Quick sanity checks you can run

```python
tests = [
    ("2024-02-29", True),   # leap year
    ("2023-02-29", False),  # not leap year
    ("1900-02-29", False),  # century non-leap
    ("2000-02-29", True),   # century leap
    ("2024-04-31", False),  # April has 30 days
    ("2024-13-01", False),  # invalid month
    ("2024-00-10", False),  # invalid month
    ("2024-01-00", False),  # invalid day
    ("2024-1-5",   False),  # missing zero-padding
    ("24-01-01",   False),  # short year
    ("2024/01/01", False),  # wrong separator
    ("0000-01-01", False),  # year zero
    ("0001-01-01", True),   # valid low year
    ("9999-12-31", True),   # valid high year
    (None,         False),  # non-string
]

for s, expected in tests:
    assert is_valid_iso_date(s) == expected, f"Failed on {s!r}"
print("All tests passed.")
```

Let me know if you want it to also accept/reject specific things like year-0000 differently, or if you need timezone-agnostic parsing added on top (though that would break the "date-only" requirement).