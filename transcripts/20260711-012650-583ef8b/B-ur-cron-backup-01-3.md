**Operating from: Bottom-Right (Build + Quality)**

### Confirming before I proceed
These are the key assumptions I'm acting on. If any are wrong, now is the time to say so:
- The script `/opt/scripts/backup.sh` exists and is executable
- You want this to run under the user account that owns the crontab (not as root or a service account, unless that's what you're setting up)
- "Weekday" means Monday–Friday (not Saturday/Sunday)
- 02:30 is in 24-hour time, in your system's local timezone
- The system has `cron` available and running (standard on Linux/Unix/macOS)
- You want output (stdout/stderr) to go to the default cron logging, or you're handling it in the script itself

### The artifact

```cron
30 2 * * 1-5 /opt/scripts/backup.sh
```

**Field breakdown:**
- `30` = minute (02:30)
- `2` = hour (02:00–03:00, 24-hour format)
- `*` = day of month (every day, filtered by weekday below)
- `*` = month (every month)
- `1-5` = day of week (Monday=1 through Friday=5)

**To install:** Add this line to your crontab by running `crontab -e`, paste the entry, save, and exit. Verify with `crontab -l`.