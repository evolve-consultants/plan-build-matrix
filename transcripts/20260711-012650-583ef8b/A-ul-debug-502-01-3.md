# Diagnosing Intermittent 502s

Start with these high-signal investigations:

## 1. **Check your actual error logs first** (30 mins)
- 502s from your load balancer/reverse proxy vs. from origin servers
- What's happening 10-30 seconds *before* the 502?
- Do they cluster or are they truly random?

This tells you if the problem is *routing* or *your service*.

## 2. **Resource exhaustion** (quick wins)
During the hour after a 502 occurs:
- Memory spikes or leaks
- Connection pool saturation (database, Redis, external APIs)
- Open file descriptor limits
- CPU throttling (especially on containers)

Check metrics 2-3 minutes *before* the error, not at the moment it happens.

## 3. **Dependency timeouts**
502s often mean "upstream service didn't respond in time." Check:
- Database query timeouts (slow queries every hour?)
- External API calls hanging
- Internal service latency spikes
- Are timeout configurations actually being honored?

## 4. **Process crashes/restarts**
- Are your app processes dying and restarting?
- Check OOM killer logs, segfaults, unhandled exceptions
- If you're doing deployments/rolling updates, that's an obvious culprit

## What to collect *right now*:
```
- Timestamps of the last 5-10 502s (exact times)
- Logs from load balancer + app servers (5 min windows around each)
- Metrics: CPU, memory, connections, queue depths
- Traffic volume at those times
- Any recent code/config changes
```

**What's your setup?** (K8s? Traditional servers? Managed service?) That shapes the next steps significantly.