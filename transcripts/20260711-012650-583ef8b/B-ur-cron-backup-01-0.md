**Operating from: Bottom-Right (Build + Quality)**

### Confirming before I proceed

These are the key assumptions I'm acting on:

- The script `/opt/scripts/backup.sh` exists and is executable
- You want the job to run as the user who owns the crontab entry (not as root or another user)
- `02:30` means 2:30 AM in the system's local timezone
- "Weekday" means Monday–Friday (not Saturday/Sunday)
- Standard cron syntax is acceptable; you don't need systemd timers or other schedulers
- Logging/error handling is managed by the script itself or by cron's default mail mechanism

### The artifact

```cron
30 2 * * 1-5 /opt/scripts/backup.sh
```

**Field breakdown:**
- `30` — minute
- `2` — hour (2 AM)
- `*` — day of month (any)
- `*` — month (any)
- `1-5` — day of week (1=Monday, 5=Friday)
- `/opt/scripts/backup.sh` — full path to script

### To install

Add this line to your crontab with `crontab -e`, or append it to a file and load it with `crontab <filename>`.

To verify it's in place: `crontab -l`

---

*(If any of those assumptions are wrong — different user, timezone handling, logging requirements — say so and I'll adjust.)*