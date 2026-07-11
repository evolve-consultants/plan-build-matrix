**Operating from: Bottom-Right (Build + Quality)**

### Confirming before I proceed
These are the key assumptions I'm acting on. If any are wrong, now is the time to say so:
- The script `/opt/scripts/backup.sh` exists and is executable
- You want the job to run as the user whose crontab this is (not as root or another user)
- "Weekday" means Monday–Friday (not Saturday–Sunday)
- The server's timezone is already correct and you're specifying 02:30 in the local timezone
- You want the cron daemon to handle all output (or you'll redirect it separately)

<assumptions>
  <project>Standard Linux/Unix system with cron service running</project>
  <task>Schedule a backup script to run automatically on weekdays at a specific time</task>
  <operator>You have access to edit a crontab and can verify the script path is correct</operator>
</assumptions>

### The artifact

```
30 2 * * 1-5 /opt/scripts/backup.sh
```

**Field breakdown:**
- `30` — minute (30)
- `2` — hour (02:00–02:59, so 02:30)
- `*` — day of month (any)
- `*` — month (any)
- `1-5` — day of week (Monday=1 through Friday=5)
- `/opt/scripts/backup.sh` — the command

**To install:** Run `crontab -e` and paste the line above into the file, save, and exit.

**To verify:** Run `crontab -l` and confirm the entry appears.