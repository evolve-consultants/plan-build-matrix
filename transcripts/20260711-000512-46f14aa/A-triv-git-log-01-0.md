# Git Command for Last 5 Commits (One Line Each)

```bash
git log -5 --oneline
```

**Breakdown:**
- `git log` — shows commit history
- `-5` — limits output to 5 commits
- `--oneline` — condenses each commit to a single line showing the abbreviated hash and commit message

**Example output:**
```
a1b2c3d Fix login bug
e4f5g6h Add user authentication
i7j8k9l Update README
m1n2o3p Refactor database queries
q4r5s6t Initial commit
```

### Useful variations:

```bash
# Include a graph of branches/merges
git log -5 --oneline --graph

# Show author and relative date too
git log -5 --oneline --format="%h %an %ar %s"

# Show one line per commit with decorations (branch/tag names)
git log -5 --oneline --decorate
```