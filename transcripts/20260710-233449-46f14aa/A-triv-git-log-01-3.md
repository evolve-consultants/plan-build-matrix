# Show last 5 commits, one line each

```bash
git log -5 --oneline
```

This displays the 5 most recent commits with their commit hash and message in a compact, single-line format.

**Alternative variations:**
- `git log --oneline -5` (order doesn't matter)
- `git log -n 5 --oneline` (using `-n` instead of just the number)
- `git log --oneline HEAD~5..HEAD` (explicitly showing the range)