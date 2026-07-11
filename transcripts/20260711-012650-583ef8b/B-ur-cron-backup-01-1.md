**Operating from: Bottom-Right (Build + Quality)**

### Confirming before I proceed

These are the key assumptions I'm acting on. If any are wrong, now is the time to say so:

- The script `/opt/scripts/backup.sh` exists and is executable
- You want the job to run as the user who owns the crontab entry (not as root or another user)
- "Weekday" means Monday–Friday (standard business definition)
- The system's cron daemon is running and the user has crontab privileges
- You want 02:30 in the system's local timezone (not UTC or a specific named zone)
- Success/failure logging is handled by the script itself or the system's cron mailer

---

### The artifact

```crontab
30 2 * * 1-5 /opt/scripts/backup.sh
```

**Field breakdown:**
- `30` — minute
- `2` — hour (02:30)
- `*` — day of month (any)
- `*` — month (any)
- `1-5` — day of week (Monday through Friday; 0=Sunday, 6=Saturday)
- `/opt/scripts/backup.sh` — command to run

---

### How to install

Add this line to your crontab with:

```bash
crontab -e
```

Then paste the entry, save, and exit. Verify with:

```bash
crontab -l
```