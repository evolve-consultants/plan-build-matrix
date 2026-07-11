# Git command to show last 5 commits, one per line

```bash
git log -5 --oneline
```

This will display the 5 most recent commits in a compact format showing:
- Commit hash (abbreviated)
- Commit message

**Example output:**
```
a1b2c3d Fix login bug
e4f5g6h Add user validation
i7j8k9l Refactor database code
m0n1o2p Update dependencies
q3r4s5t Initial commit
```

You can also use `git log --oneline -5` (same thing, just different order of flags).