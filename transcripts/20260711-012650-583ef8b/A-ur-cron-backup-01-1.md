# Crontab Entry

```cron
30 2 * * 1-5 /opt/scripts/backup.sh
```

## Field Breakdown
- `30` – Minute (30)
- `2` – Hour (02:00 in 24-hour format)
- `*` – Day of month (any)
- `*` – Month (any)
- `1-5` – Day of week (Monday through Friday)

## Assumptions

1. **Script Location**: `/opt/scripts/backup.sh` exists and is readable by the cron user

2. **Executable Permission**: The script has execute permissions (`chmod +x /opt/scripts/backup.sh`)

3. **Cron User**: The entry is added to a user's crontab (via `crontab -e`) or root's crontab—whoever needs to run this backup

4. **Shell Environment**: The system's default shell (`/bin/sh` or similar) can execute the script, OR the script includes a proper shebang (e.g., `#!/bin/bash`)

5. **Working Directory**: Any relative paths in the script are either absolute or the script handles them independently (cron runs with a minimal environment)

6. **Time Zone**: The system's local time zone applies; if you need UTC or a different zone, set it explicitly in the crontab or script

7. **Output Handling**: By default, cron output goes to the user's mail. To suppress it or log elsewhere, append:
   ```cron
   30 2 * * 1-5 /opt/scripts/backup.sh >> /var/log/backup.log 2>&1
   ```

8. **Dependencies**: Any commands, databases, or services the backup script requires are available and functioning at 02:30