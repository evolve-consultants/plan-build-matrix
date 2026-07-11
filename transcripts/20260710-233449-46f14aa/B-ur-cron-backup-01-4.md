**Operating from: Bottom-Right (Build + Quality)**

### Confirming before I proceed

These are the key assumptions I'm acting on. If any are wrong, now is the time to say so:

- The script `/opt/scripts/backup.sh` exists and is executable
- You want it to run at 02:30 (2:30 AM) in the system's local timezone
- "Weekday" means Monday–Friday (not Saturday or Sunday)
- The cron job should run under the current user's crontab (or you'll specify which user if it's a system cron)
- The script handles its own logging; if it doesn't, you'll redirect output separately
- No special environment variables or shell are required beyond the default

---

```bash
30 2 * * 1-5 /opt/scripts/backup.sh
```

**Field breakdown:**
- `30` — minute (02:30)
- `2` — hour (2 AM)
- `*` — day of month (every day)
- `*` — month (every month)
- `1-5` — day of week (Monday=1 through Friday=5)

**To install:**
```bash
crontab -e
# Paste the line above, save and exit
```

**If you need output logged:**
```bash
30 2 * * 1-5 /opt/scripts/backup.sh >> /var/log/backup.log 2>&1
```