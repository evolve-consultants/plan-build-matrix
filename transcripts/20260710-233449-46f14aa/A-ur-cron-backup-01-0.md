# Crontab Entry

```cron
30 2 * * 1-5 /opt/scripts/backup.sh
```

## Explanation

- `30` - Minute (30)
- `2` - Hour (02:00, 24-hour format)
- `*` - Day of month (any)
- `*` - Month (any)
- `1-5` - Day of week (Monday-Friday)
- `/opt/scripts/backup.sh` - Command to execute

## Assumptions

1. **Script location**: `/opt/scripts/backup.sh` exists and is readable by the cron user
2. **Script permissions**: The script has execute permissions (`chmod +x`)
3. **Cron user**: The user running this cron job has:
   - Permission to execute the script
   - Access to any resources the script needs (files, directories, commands)
4. **Working directory**: The script uses absolute paths OR is self-contained with relative path handling
5. **System timezone**: The system's timezone is configured correctly; "02:30" is interpreted in the system's local time
6. **Dependencies**: Any required commands, binaries, or services that `backup.sh` calls are available and in the user's `PATH`
7. **Logging**: Output will be sent to the cron user's mailbox (if mailing is configured); redirect output explicitly if preferred:
   ```cron
   30 2 * * 1-5 /opt/scripts/backup.sh >> /var/log/backup.log 2>&1
   ```