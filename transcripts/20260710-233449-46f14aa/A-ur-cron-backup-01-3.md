# Crontab entry for weekday backup

```cron
30 02 * * 1-5 /opt/scripts/backup.sh
```

## Field breakdown:
- `30` – minute (30)
- `02` – hour (02:30, 24-hour format)
- `*` – day of month (any)
- `*` – month (any)
- `1-5` – day of week (Monday-Friday)

## Assumptions:

1. **Script location**: `/opt/scripts/backup.sh` exists and is executable (`chmod +x`)

2. **Shell interpreter**: The script has a proper shebang line (e.g., `#!/bin/bash`) and will execute with the cron default shell (typically `/bin/sh`)

3. **Timezone**: The system timezone is configured correctly; cron uses the system's local time

4. **Permissions**: The user running cron has execute permission on the script and read/write access to any directories it needs

5. **Environment variables**: The script either:
   - Doesn't rely on environment variables set in shell rc files, or
   - Defines its own (cron runs with minimal environment)

6. **Logging**: Output will be emailed to the cron user (or discarded) unless redirected; consider adding:
   ```cron
   30 02 * * 1-5 /opt/scripts/backup.sh >> /var/log/backup.log 2>&1
   ```

7. **Day of week**: Uses Monday=1, Sunday=7 convention (standard in most Unix systems; some use Sunday=0)