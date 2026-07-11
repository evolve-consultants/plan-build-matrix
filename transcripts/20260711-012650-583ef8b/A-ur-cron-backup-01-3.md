# Crontab entry for weekday backup

```cron
30 2 * * 1-5 /opt/scripts/backup.sh
```

## Breakdown
- `30` – Minute (30)
- `2` – Hour (02:30, 24-hour format)
- `*` – Day of month (any)
- `*` – Month (any)
- `1-5` – Day of week (Monday–Friday)
- `/opt/scripts/backup.sh` – Full path to script

## Assumptions

1. **Script existence & permissions**: `/opt/scripts/backup.sh` exists and is executable by the cron user
2. **Cron daemon**: `crond` or equivalent is running on the system
3. **User context**: The script will run as the user whose crontab this is entered into (use `sudo crontab -e` for root, or regular user for their own crontab)
4. **Timezone**: System timezone is correct; cron uses local system time
5. **Dependencies**: All required binaries/paths referenced in the script are available in the cron environment (PATH may be limited in cron; consider using absolute paths in the script)
6. **Email notifications**: Any script output/errors will be mailed to the cron user (if `MAILTO` is set); redirect output if preferred:
   ```cron
   30 2 * * 1-5 /opt/scripts/backup.sh >> /var/log/backup.log 2>&1
   ```
7. **No special logging**: Cron job output handling relies on system defaults; explicit logging is recommended for production scripts