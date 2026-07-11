**Operating from: Bottom-Right (Build + Quality)**

### Confirming before I proceed
- The script exists at `/opt/scripts/backup.sh` and is executable
- The user running cron (or the system crontab) has permission to execute it
- You want the job to run every Monday through Friday, not just on business holidays
- Output/errors can go to the system default (usually mailed to the cron user) or you'll handle redirection separately
- The system uses standard Unix cron syntax (not all systems do — some use variants)

<assumptions>
  <project>Standard Linux/Unix system with cron daemon running</project>
  <task>Schedule a backup script to run at 2:30 AM on weekdays only</task>
  <operator>Familiar with crontab but want a clean, documented entry</operator>
</assumptions>

### The entry

```cron
30 2 * * 1-5 /opt/scripts/backup.sh
```

**Field breakdown:**
- `30` — minute (30)
- `2` — hour (02:30 in 24-hour time)
- `*` — day of month (any)
- `*` — month (any)
- `1-5` — day of week (Monday=1 through Friday=5)

### To install
Add this line to your crontab:
```bash
crontab -e
```

Then paste the entry and save. Verify with:
```bash
crontab -l
```

If you want to capture output or suppress mail notifications, add redirection:
```cron
30 2 * * 1-5 /opt/scripts/backup.sh >> /var/log/backup.log 2>&1
```