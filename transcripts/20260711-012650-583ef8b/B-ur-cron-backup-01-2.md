**Operating from: Bottom-Right (Build + Quality)**

### Confirming before I proceed
- The script `/opt/scripts/backup.sh` exists and is executable
- You want 02:30 (2:30 AM) in the system's local timezone
- "Weekday" means Monday–Friday (not Saturday/Sunday)
- The cron job runs under the user account that owns the script (or has permission to execute it)
- You're comfortable with cron's default behavior: no email unless the job produces output or fails
- The system uses standard cron syntax (Linux/Unix/macOS)

<assumptions>
  <project>Standard cron daemon available; no special job scheduler (systemd timer, etc.) in use</project>
  <task>Automated backup execution on a regular weekday schedule</task>
  <operator>You can edit crontab directly (via `crontab -e` or similar) and own the user account where this will run</operator>
</assumptions>

### The artifact

```crontab
30 2 * * 1-5 /opt/scripts/backup.sh
```

**Field breakdown:**
- `30` — minute (30)
- `2` — hour (02:30, 24-hour format)
- `*` — day of month (any)
- `*` — month (any)
- `1-5` — day of week (Monday=1 through Friday=5; Sunday=0)
- `/opt/scripts/backup.sh` — command to execute

**To install:**
```bash
crontab -e
# Paste the line above, save and exit
```

**To verify it was added:**
```bash
crontab -l
```

---

*If any assumption is wrong (different timezone handling needed, different day-of-week numbering, email/logging preferences, etc.), say so and I'll adjust.*