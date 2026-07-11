# Show last 5 commits, one line each

```bash
git log --oneline -5
```

Or if you want to see all branches:

```bash
git log --oneline -5 --all
```

The `--oneline` flag condenses each commit to a single line showing the commit hash and message.