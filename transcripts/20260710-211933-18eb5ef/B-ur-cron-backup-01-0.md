**Operating from: Bottom-Right (Build + Quality)**

### Confirming before I proceed

These are the key assumptions I'm acting on. If any are wrong, now is the time to say so:

- The script `/opt/scripts/backup.sh` exists and is executable
- You want the job to run at 02:30 (2:30 AM) in the system's local timezone
- "Weekday" means Monday–Friday (not Saturday/Sunday)
- You're comfortable with cron's default behavior: runs under the user who owns the crontab, inherits a minimal environment, logs output to syslog
- You don't need explicit success/failure notifications (if you do, we should add `| mail` or similar)
- The script handles its own logging or you're okay with cron's default

### The artifact

```cron
30 2 * * 1-5 /opt/scripts/backup.sh
```

**Field breakdown:**
- `30` = minute 30
- `2` = hour 02 (24-hour format)
- `*` = any day of month
- `*` = any month
- `1-5` = Monday through Friday (1=Mon, 5=Fri)

**To install:** paste this into `crontab -e` and save.

**If you need stderr captured too:**
```cron
30 2 * * 1-5 /opt/scripts/backup.sh >> /var/log/backup.log 2>&1
```

This appends stdout and stderr to a log file. Rotate it with logrotate if it grows large.