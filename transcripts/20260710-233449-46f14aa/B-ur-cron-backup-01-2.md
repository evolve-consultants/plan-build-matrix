**Operating from: Upper-Right (Build + Verify)**

### What I understand you're asking
You want a crontab line that executes `/opt/scripts/backup.sh` at 2:30 AM on Monday through Friday.

<assumptions>
  <project>The script exists at `/opt/scripts/backup.sh` and is executable. No special environment variables are required beyond what cron provides by default.</project>
  <task>You need this to run automatically on a weekday schedule with no manual intervention.</task>
  <operator>You're comfortable with standard cron syntax and have access to `crontab -e` or similar. You own verification that the script runs as expected.</operator>
</assumptions>

### The artifact

```cron
30 2 * * 1-5 /opt/scripts/backup.sh
```

**Field breakdown:**
- `30` — minute (30)
- `2` — hour (02:00 in 24-hour format)
- `*` — day of month (any)
- `*` — month (any)
- `1-5` — day of week (1=Monday, 5=Friday)

### What I'm confident about
- Syntax is correct and standard across Linux/Unix cron implementations
- Will execute at 02:30 every weekday

### What I'd double-check
- **Script permissions**: confirm `/opt/scripts/backup.sh` has execute bit set (`chmod +x`). If cron can't execute it, the job will silently fail.
- **User context**: determine which user should run this (usually your own user or root). Add it to the appropriate crontab — if you're not running as the target user, use `sudo crontab -e -u <username>` instead of `crontab -e`.
- **Output handling**: by default, cron mails output to the user. If the script is noisy or you want logs elsewhere, redirect explicitly:
  ```cron
  30 2 * * 1-5 /opt/scripts/backup.sh >> /var/log/backup.log 2>&1
  ```
- **Environment variables**: if the script depends on `$PATH`, `$HOME`, or other variables, you may need to source them inside the script or set them in the crontab file itself.