# Debugging Intermittent 502s

Start with the **basics** before diving deep—these catch most cases:

## Immediate checks (5 min)

**1. Is it actually your API or upstream?**
- Check your load balancer/reverse proxy logs (nginx, HAProxy, ALB)
- A 502 from nginx usually means it couldn't reach your backend at all
- Look for connection refused, timeouts, or socket errors

**2. Resource exhaustion**
```bash
# During/after a 502 occurrence
free -h              # Memory
df -h                # Disk space
vmstat 1 5           # CPU context switches (high = thrashing)
netstat -an | grep CLOSE_WAIT | wc -l  # Leaked connections?
```

**3. Process crashes**
- Check if your application process is actually running
- Look at systemd journal or supervisor logs for exit codes
- Restart frequency spike during 502 windows?

## Second round (15 min)

**4. Connection pool exhaustion**
This is the most common culprit for "no pattern" 502s:
- Database connections maxed out?
- HTTP client connection pools drained?
- Add logging: log pool utilization, active/waiting connections
```python
# Example: what's actually happening
logger.info(f"DB pool: {pool.size()}/{pool.max_size()}, active={pool.active()}")
```

**5. Specific request patterns**
- Is 502 correlated with certain endpoints? (`grep 502 access.log | awk '{print $7}' | sort | uniq -c`)
- Slow queries blocking your pool?
- External API timeouts (if you call one)?

**6. Graceful shutdown issues**
- Are you deploying during the 502s?
- Check if old processes aren't draining connections before exiting

## What to add *now*

Even if you don't find it, these will help next time:

```python
# Log backend health at your load balancer layer
upstream_response_time = response_time
if upstream_response_time > 30s or status == 502:
    log(request_id, endpoint, pool_usage, active_connections, 
        slow_query_log_entries_in_last_5s)
```

- **Add request tracing IDs** so you can correlate with backend logs
- **Graph pool utilization** - even if you're not at max, saturation patterns appear before crashes
- **Alert on 502 rate**, not just presence

## Fastest way to confirm

If you have 1 hour between 502s, **instrument the next one**:
- SSH in during business hours
- Run `watch -n 1 'your_monitoring_command'` 
- Trigger load if possible, capture the exact moment a 502 happens
- Check: process count, memory, connection states, error logs

**Most likely scenario**: a slow query or external API timeout is blocking your connection pool once an hour when a batch job runs, or traffic hits a certain threshold.

What's your stack (language, web framework, database)?