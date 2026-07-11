# Show last 5 commits, one line each

```bash
git log -5 --oneline
```

This will display the 5 most recent commits with their short hash and commit message on a single line each.

If you want to see more details while still keeping it compact, you can also use:

```bash
git log -5 --pretty=format:"%h %s"
```

Where `%h` is the short hash and `%s` is the subject line.