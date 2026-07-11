# Crontab Entry

```cron
30 2 * * 1-5 /opt/scripts/backup.sh
```

## Field Breakdown
- `30` – minute (30)
- `2` – hour (02:00, 24-hour format)
- `*` – day of month (any)
- `*` – month (any)
- `1-5` – day of week (Monday–Friday)
- `/opt/scripts/backup.sh` – command to execute

## Assumptions

1. **Script exists and is executable**
   - `/opt/scripts/backup.sh` exists with executable permissions (`chmod +x`)

2. **Cron daemon is running**
   - The system has an active cron service (crond/cron)

3. **User context**
   - Entry is added to a user's crontab (`crontab -e`) or root's crontab
   - The executing user has read/execute permissions on the script and write permissions on any target directories

4. **Timezone**
   - Times are interpreted in the **system's local timezone** (set via `/etc/timezone` or `/etc/localtime`)

5. **Shell and PATH**
   - Cron runs with a minimal shell (usually `/bin/sh`) and limited PATH
   - Script should use **absolute paths** for any commands it calls
   - Consider adding a shebang: `#!/bin/bash` at the start of `backup.sh`

6. **Output handling**
   - Script output will be logged by cron (check `/var/log/syslog` or mail to the cron user)
   - For silent operation, redirect: `30 2 * * 1-5 /opt/scripts/backup.sh > /dev/null 2>&1`

7. **No special environment variables**
   - Script should not rely on user-specific env vars (`$HOME`, `$USER`, etc.) unless explicitly set in crontab