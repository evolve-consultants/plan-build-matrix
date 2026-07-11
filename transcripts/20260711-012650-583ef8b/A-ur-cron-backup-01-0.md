# Crontab Entry

```cron
30 2 * * 1-5 /opt/scripts/backup.sh
```

## Field Breakdown
- `30` – Minute (30)
- `2` – Hour (02:30 in 24-hour format)
- `*` – Day of month (every day)
- `*` – Month (every month)
- `1-5` – Day of week (Monday through Friday)

## Environment Assumptions

1. **Script Permissions**: `/opt/scripts/backup.sh` is executable (`chmod +x`)

2. **Shell Interpreter**: The script has a proper shebang line (e.g., `#!/bin/bash`) to specify its interpreter

3. **Absolute Paths**: Any commands or file paths in the script use absolute paths, since cron has a minimal PATH environment

4. **User Context**: The entry is in the appropriate user's crontab (e.g., `crontab -e` as the user who needs to run it), or in `/etc/cron.d/` with a username field specified:
   ```cron
   30 2 * * 1-5 root /opt/scripts/backup.sh
   ```

5. **Logging/Output**: The script handles its own logging, or you may want to redirect output:
   ```cron
   30 2 * * 1-5 /opt/scripts/backup.sh >> /var/log/backup.log 2>&1
   ```

6. **Dependencies**: Any required services (database, network mounts, etc.) are available at 02:30 AM

7. **Timezone**: The system timezone is correct; cron uses local system time