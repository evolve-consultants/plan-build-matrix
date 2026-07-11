# Diagnosing Intermittent 502s

Start with **the basics first**, then narrow from there:

## Immediate checks

**1. Check upstream dependencies**
- Load balancer / reverse proxy logs (nginx, HAProxy, etc.)
- Backend service logs during 502 windows
- Are *all* backends returning 502 or just some?
  - If some: scale/restart those instances
  - If all: points to a shared dependency

**2. Timing correlation**
- Pull logs from 10 minutes before/after each 502
- Check for: deployments, scheduled jobs, cache clears, batch operations, cost-saving auto-scaling events
- Graph request volume, latency, error rate together

**3. Resource exhaustion (most common culprit)**
```
- Memory: check for memory leaks in your app (growing over time?)
- Connections: DB connections, file descriptors, open sockets
- Disk: /tmp full? log rotation issues?
- CPU: are processes getting killed under load?
```

## Next tier

**4. Check your actual app**
- Add detailed logging to request entry/exit
- What's the *last* log before the 502? (usually nothing = process crash)
- Are you hitting timeout limits in your app framework?

**5. Dependency health**
- Database: slow queries causing timeouts?
- Cache layer: evictions, connection timeouts?
- External APIs: are *they* timing out, causing cascade?

## How to instrument this

Rather than guess, add observability:
```python
# Rough example - add timings to everything
start = time.time()
try:
    result = call_db()
    log(f"db_call: {time.time()-start}s")
except Timeout:
    log("db_call: TIMEOUT")
```

Then **watch the actual 502 window** with logs + metrics side-by-side.

---

**What do your logs show when a 502 happens?** That's the real clue.