# Crontab Entry

```cron
30 2 * * 1-5 /opt/scripts/backup.sh
```

## Field Breakdown
- `30` – minute (30)
- `2` – hour (02:30 in 24-hour format)
- `*` – day of month (any)
- `*` – month (any)
- `1-5` – day of week (Monday through Friday)

## Environment Assumptions

1. **Script Location**: `/opt/scripts/backup.sh` exists and is readable by the cron user

2. **Executable Permission**: The script has execute permissions (`chmod +x /opt/scripts/backup.sh`)

3. **Shebang Line**: The script contains a proper shebang (e.g., `#!/bin/bash`) as the first line

4. **Cron User**: The entry is in the appropriate user's crontab or `/etc/cron.d/` with a user field specified

5. **Shell**: Uses the default shell configured for the cron daemon (usually `/bin/sh`)

6. **PATH**: Any commands in the script are either fully qualified or available in the cron environment's PATH

7. **Working Directory**: The script doesn't assume a specific working directory; use absolute paths within the script

8. **Timezone**: Assumes the system's local timezone; use `TZ=UTC` above the entry if UTC is required

## Recommended Enhancement

```cron
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin
30 2 * * 1-5 /opt/scripts/backup.sh >> /var/log/backup.log 2>&1
```

This adds logging and explicitly defines the shell and PATH.