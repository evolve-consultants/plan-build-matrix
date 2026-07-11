**Operating from: Bottom-Right (Build + Quality)**

### Confirming before I proceed

These are the key assumptions I'm acting on. If any are wrong, now is the time to say so:

- The script `/opt/scripts/backup.sh` exists and is executable
- You want this to run on the local machine (not a remote host)
- The user running cron has permission to execute the script
- "Weekday" means Monday–Friday (not Saturday/Sunday)
- 02:30 in 24-hour format is the intended time
- The script should run under the current user's cron (not system crontab or a different user)
- No special output handling is needed (cron's default email-on-error is acceptable)

---

### The artifact

```bash
30 2 * * 1-5 /opt/scripts/backup.sh
```

**Field breakdown:**
- `30` — minute
- `2` — hour (02:00–03:00, 24-hour format)
- `*` — day of month (any)
- `*` — month (any)
- `1-5` — day of week (1=Monday, 5=Friday)

**To install:**
```bash
crontab -e
```
Then paste the entry above into your editor, save, and exit.

**To verify:**
```bash
crontab -l
```

---

### Optional refinements

If you want to capture output or suppress errors:

```bash
30 2 * * 1-5 /opt/scripts/backup.sh >> /var/log/backup.log 2>&1
```

This appends stdout and stderr to `/var/log/backup.log` instead of emailing you.