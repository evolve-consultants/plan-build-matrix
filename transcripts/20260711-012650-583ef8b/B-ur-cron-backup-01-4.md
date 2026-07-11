**Operating from: Bottom-Right (Build + Quality)**

### Confirming before I proceed
These are the key assumptions I'm acting on. If any are wrong, now is the time to say so:
- The script `/opt/scripts/backup.sh` exists and is executable
- You want the job to run under the current user's crontab (not root or a service account)
- 02:30 means 2:30 AM in your system's local timezone
- "Weekday" means Monday–Friday (exclude Saturday and Sunday)
- You want the job to run silently (no email output) or you have mail configured
- No special environment variables are needed beyond what cron inherits by default

### The artifact

```cron
30 2 * * 1-5 /opt/scripts/backup.sh
```

**Field breakdown:**
- `30` — minute (30)
- `2` — hour (02:00 in 24-hour format)
- `*` — day of month (every day)
- `*` — month (every month)
- `1-5` — day of week (Monday=1 through Friday=5)

### To install
1. Open your crontab editor: `crontab -e`
2. Paste the line above
3. Save and exit

### If you need to redirect output
Add one of these to the end of the line:

- Discard all output: `> /dev/null 2>&1`
- Log to a file: `>> /var/log/backup.log 2>&1`
- Email on error only: `2>&1 | grep -q . && mail -s "Backup failed" you@example.com`

Example with logging:
```cron
30 2 * * 1-5 /opt/scripts/backup.sh >> /var/log/backup.log 2>&1
```