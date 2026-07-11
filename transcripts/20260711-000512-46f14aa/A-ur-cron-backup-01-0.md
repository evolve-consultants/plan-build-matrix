# Crontab Entry

```
30 2 * * 1-5 /opt/scripts/backup.sh
```

## Field Breakdown

| Field | Value | Meaning |
|-------|-------|---------|
| Minute | `30` | At minute 30 |
| Hour | `2` | At hour 2 (2 AM) |
| Day of Month | `*` | Any day |
| Month | `*` | Any month |
| Day of Week | `1-5` | Monday through Friday |

So this runs at **02:30 AM, Monday–Friday**.

## Assumptions

1. **Day-of-week numbering**: Standard cron uses `0` or `7` for Sunday, `1` for Monday, ..., `6` for Saturday. This assumes a standard Vixie-cron/cronie-style parser (used on most Linux distros). `1-5` = Mon–Fri.

2. **Time zone**: Cron uses the system's local time zone (as configured in `/etc/timezone` or `TZ` environment variable for the cron daemon), not UTC — unless explicitly overridden. If the server's timezone differs from what you expect (e.g., server is in UTC but you want 2:30 AM in a different zone), you'll need to either adjust the hour value or set `CRON_TZ=<Zone>` as a line above the entry (supported in some cron implementations like cronie):
   ```
   CRON_TZ=America/New_York
   30 2 * * 1-5 /opt/scripts/backup.sh
   ```

3. **Script permissions**: `/opt/scripts/backup.sh` is assumed to already have execute permission (`chmod +x`) and the correct shebang line (e.g., `#!/bin/bash`) so cron can invoke it directly.

4. **User context**: This entry is assumed to be added via `crontab -e` for a specific user (e.g., root or a service account) who has the necessary permissions to run the backup script and access whatever files/directories it operates on. If placed in `/etc/crontab` or `/etc/cron.d/`, an explicit user field would be required between the schedule and the command, e.g.:
   ```
   30 2 * * 1-5 root /opt/scripts/backup.sh
   ```

5. **PATH and environment**: Cron jobs run with a minimal environment (often just `/usr/bin:/bin` for PATH, no interactive shell profile loaded). If `backup.sh` relies on environment variables or a specific `PATH` (e.g., to find other binaries it calls), you may need to either:
   - Set `PATH` explicitly at the top of the crontab, or
   - Have the script itself source any needed environment/profile settings.

6. **Logging**: No output redirection is specified. By default, cron typically emails command output to the crontab owner (if mail is configured) or discards it silently depending on system config. If you want to capture logs, you'd typically append something like:
   ```
   30 2 * * 1-5 /opt/scripts/backup.sh >> /var/log/backup.log 2>&1
   ```

If any of these assumptions don't match your actual setup (e.g., different cron implementation, timezone requirements, or logging needs), let me know and I can adjust the entry.