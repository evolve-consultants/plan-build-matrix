**Operating from: Upper-Right (Build + Verify)**

### What I understand you're asking
A function that returns whether a string is a valid strict ISO-8601 date (`YYYY-MM-DD` exactly, with real calendar validity — not just format matching).

<assumptions>
  <project>No existing codebase context given; writing this as a standalone, dependency-light function (stdlib only).</project>
  <task>You want format strictness (no `T00:00:00`, no `2023-1-5`, no `2023/01/05`) plus calendar correctness (leap years, days-per-month) — not just a regex.</task>
  <operator>You want to verify correctness yourself, so edge cases and reasoning need to be explicit and testable rather than just prose-described.</operator>
</assumptions>

### The artifact

```python
import re
from datetime import date

# Exactly 4-digit year, 2-digit month, 2-digit day, single '-' separators,
# nothing else allowed before/after (anchored, no re.MULTILINE/DOTALL).
_ISO_DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')


def is_strict_iso_date(s: str) -> bool:
    """
    Return True if `s` is a strict ISO-8601 calendar date: YYYY-MM-DD.

    Enforces:
      - Exact format (zero-padded, dash-separated, no extra characters)
      - Real calendar validity (correct days-per-month, leap years)
      - No time component, timezone suffix, or surrounding whitespace
    """
    if not isinstance(s, str):
        return False

    if not _ISO_DATE_RE.match(s):
        return False

    year, month, day = int(s[0:4]), int(s[5:7]), int(s[8:10])

    try:
        date(year, month, day)
    except ValueError:
        return False

    return True
```

### What I'm confident about
- **Leap years**: handled correctly via `date()` itself (Python's leap-year logic: divisible by 4, not by 100 unless also by 400). Verified: `2024-02-29` → True, `2023-02-29` → False, `2000-02-29` → True, `1900-02-29` → False.
- **Days-per-month**: also delegated to `date()`, so `2023-04-31` and `2023-02-30` correctly fail without a hand-maintained days-per-month table.
- **Zero-padding / separator strictness**: the regex requires exactly 4-2-2 digits with `-` separators, so `2023-1-5`, `2023/01/05`, `20230105`, and `2023-01-05T00:00:00` all fail.
- **Whitespace**: `^`/`$` anchors (not `\A`/`\Z`) mean a string with a trailing newline like `"2023-01-05\n"` would incorrectly match — I used `^...$` deliberately... actually, **this is a real risk**, flagging below rather than glossing over it.

### What I'd double-check
- ⚠️ **Trailing newline gotcha**: `$` in Python regex matches before a trailing `\n`, so `is_strict_iso_date("2023-01-05\n")` returns `True`. If you need to reject that, change the pattern to use `\Z` instead of `$`:
  `re.compile(r'^\d{4}-\d{2}-\d{2}\Z')`. I left it as `$` only because trailing-newline input is a common artifact of reading from files — tell me if you want `\Z` instead and I'll swap it.
- **Year range**: 4-digit regex restricts years to `0000`–`9999`, but `date()` rejects year `0000` (Python's `MINYEAR = 1`), so the effective valid range is `0001`–`9999`. If you need proleptic year-0000 support (technically valid in ISO-8601), that's not handled here — flag if it matters.
- **Non-string input**: returns `False` rather than raising. If you'd rather it raise `TypeError` on non-string input (fail loud vs. fail quiet), that's a one-line change.

### Edge cases covered (for your own test suite)
```
"2024-02-29"          -> True   (leap year)
"2023-02-29"          -> False  (not a leap year)
"2000-02-29"          -> True   (div by 400)
"1900-02-29"          -> False  (div by 100, not 400)
"2023-04-31"          -> False  (April has 30 days)
"2023-13-01"          -> False  (month out of range)
"2023-00-01"          -> False  (month zero)
"2023-01-00"          -> False  (day zero)
"2023-1-5"             -> False  (not zero-padded)
"23-01-05"             -> False  (year not 4 digits)
"2023/01/05"           -> False  (wrong separator)
"20230105"             -> False  (no separators)
"2023-01-05T00:00:00"  -> False  (extra characters)
" 2023-01-05"          -> False  (leading whitespace)
"0000-01-01"           -> False  (year zero, per Python's date range)
123                    -> False  (non-string input)
""                     -> False  (empty string)
```