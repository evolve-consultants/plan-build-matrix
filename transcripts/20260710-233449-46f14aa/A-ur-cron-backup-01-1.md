# Crontab Entry

```cron
30 2 * * 1-5 /opt/scripts/backup.sh
```

## Breakdown

- `30` — minute (30)
- `2` — hour (02:00, 24-hour format)
- `*` — day of month (any)
- `*` — month (any)
- `1-5` — day of week (Monday–Friday)
- `/opt/scripts/backup.sh` — command to execute

## Assumptions

1. **Script is executable** — The script has execute permissions (`chmod +x /opt/scripts/backup.sh`)

2. **Absolute path** — Using the full path `/opt/scripts/backup.sh` rather than a relative path (safer for cron jobs, which don't inherit shell working directories)

3. **Shell environment** — The default shell (`/bin/sh`) can execute the script, or the script has an appropriate shebang (e.g., `#!/bin/bash`)

4. **User permissions** — The cron job runs under a user with:
   - Read/execute permissions on `/opt/scripts/backup.sh`
   - Permissions to access any files/directories the backup needs

5. **No user interaction** — The script runs non-interactively (no prompts or password requirements)

6. **Output handling** — Output will be mailed to the cron user (if desired, redirect with `>> /var/log/backup.log 2>&1`)

7. **Time zone** — The system's local time zone applies (check with `date` or `/etc/timezone`)