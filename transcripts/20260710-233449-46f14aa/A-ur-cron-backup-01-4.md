# Crontab entry for weekday backup

```cron
30 2 * * 1-5 /opt/scripts/backup.sh
```

## Assumptions about the environment:

1. **Script location**: `/opt/scripts/backup.sh` exists and is executable
2. **Permissions**: The cron user has execute permissions on the script
3. **Shell**: The system uses a standard Unix/Linux shell (bash, sh, etc.)
4. **Time zone**: The system's local time zone is correctly configured; cron uses local system time
5. **Weekday definition**: Monday-Friday (1-5 in cron's day-of-week field, where 0=Sunday, 6=Saturday)
6. **User context**: The job will run as the user who owns the crontab (typically the user running `crontab -e`)
7. **Output handling**: Any output will be mailed to the cron user's local mailbox (unless configured otherwise)
8. **Dependencies**: All required commands, paths, and environment variables needed by `backup.sh` are available in the cron environment (which is minimal by default)

## Related considerations:

If you need to **ensure email delivery** or **capture logs**, consider:
```cron
30 2 * * 1-5 /opt/scripts/backup.sh >> /var/log/backup.log 2>&1
```

If the script requires **specific environment variables**, add them above the crontab entry:
```cron
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin
30 2 * * 1-5 /opt/scripts/backup.sh
```