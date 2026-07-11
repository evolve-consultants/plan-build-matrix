**Operating from: Bottom-Right (Build + Quality)**

### Confirming before I proceed
- "Weekday" means Monday–Friday (not a specific day named "weekday").
- 02:30 refers to the system's local time as seen by cron, not necessarily UTC — cron uses whatever timezone the OS/user's crontab is configured with.
- This is standard Vixie/cronie cron syntax (Linux), not a nonstandard variant (e.g., not Quartz or systemd timer syntax).
- `/opt/scripts/backup.sh` is already executable (`chmod +x`) and has a correct shebang line.
- No output redirection/logging is required — cron will mail results to the local user by default if MAILTO is configured, otherwise output is discarded depending on system config.

<assumptions>
  <project>No specific OS/distro mentioned — assuming a standard Linux system with cron or cronie installed and enabled.</project>
  <task>You want a ready-to-use crontab line, likely to add via `crontab -e` or a file in /etc/cron.d/.</task>
  <operator>Comfortable editing crontab directly; no request for logging, error handling, or locking (e.g., flock) — kept minimal per the ask.</operator>
</assumptions>

### The artifact

```
30 2 * * 1-5 /opt/scripts/backup.sh
```

If you want output logged instead of relying on cron's mail behavior:

```
30 2 * * 1-5 /opt/scripts/backup.sh >> /var/log/backup.log 2>&1
```