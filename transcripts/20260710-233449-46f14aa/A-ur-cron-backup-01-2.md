# Crontab entry for weekday backup

```crontab
30 2 * * 1-5 /opt/scripts/backup.sh
```

## Assumptions about the environment:

1. **Shell interpreter**: Uses the default shell specified in `/etc/passwd` for the user (typically `/bin/bash` or `/bin/sh`)

2. **Script executability**: `/opt/scripts/backup.sh` has execute permissions (`chmod +x`)

3. **Script shebang**: The script includes a proper shebang line (e.g., `#!/bin/bash`)

4. **Working directory**: The script either uses absolute paths or doesn't depend on a specific working directory (cron jobs run from the user's home directory by default)

5. **PATH variable**: All commands called within the script use absolute paths, or the necessary directories are in the cron `PATH` environment variable

6. **Timezone**: The system's timezone is configured correctly (cron uses system time)

7. **User permissions**: The user running the cron job has permissions to:
   - Execute the script
   - Access any files/directories the script needs
   - Write any output files

8. **Logging**: Standard output and standard error are not redirected (they'll be mailed to the cron user by default; consider redirecting them in production)

## Production recommendation:

```crontab
30 2 * * 1-5 /opt/scripts/backup.sh >> /var/log/backup.log 2>&1
```

This explicitly logs output and prevents mail delivery overhead.