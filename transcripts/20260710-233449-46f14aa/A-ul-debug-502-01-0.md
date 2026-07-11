# Debugging Intermittent 502s

Start with the **fundamentals** before diving into logs:

## Immediate triage (next 30 mins)

**1. Check upstream dependencies**
- Database connection pool exhaustion? (logs: "too many connections")
- Downstream service timeouts? (check their status pages/logs)
- Load balancer health checks passing? (may be incorrectly marking backends unhealthy)

**2. Correlate with your metrics**
- Plot 502 rate against: CPU, memory, connection count, request latency
- Is it tied to traffic spikes, or truly random?
- Are *all* servers returning 502 or just some?

**3. Look at timing**
- `grep "502" access.log` + timestamps
- Do they cluster in 30-60 second bursts, or isolated?
- Any correlation with deployments, cron jobs, backups?

## Likely culprits (in order of frequency)

| Cause | How to spot |
|-------|-----------|
| **Worker/thread pool exhaustion** | Requests queue indefinitely; new requests hit timeout | 
| **Slow downstream call** (DB/cache/API) | Response times spike 1-2 mins before 502s appear |
| **Memory leak** | Memory creeps up hour-over-hour until crash/restart |
| **File descriptor limits** | `ulimit -n`, check `/proc/[pid]/fd` on affected process |
| **Zombie connections** | `netstat -an \| grep TIME_WAIT` growing unbounded |

## What to capture NOW

Before it happens again, set up:
- **Application error logs** at the moment of 502 (full stack trace)
- **System metrics** sampled every 10s: memory, connections, CPU, goroutines/threads
- **Request timing** percentiles (p50/p95/p99) — slowdown precedes crashes
- **Application-specific**: active requests, queue depth, worker availability

## Quick wins to try

1. **Increase timeouts** on downstream calls (if you're timing out, client sees 502)
2. **Add circuit breaker** on external dependencies
3. **Check file descriptor limits**: `cat /proc/sys/fs/file-max`
4. **Restart periodically** if it's a slow leak (temporary fix, not root cause)

**What's your stack?** (language, framework, architecture) — answers differ for Python vs Node vs Go.