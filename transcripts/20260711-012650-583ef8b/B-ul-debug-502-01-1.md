**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You have a production API that sporadically returns 502 Bad Gateway errors (~once/hour) with no obvious trigger. You need a systematic way to narrow down the cause before diving into fixes.

<assumptions>
  <project>You have access to logs, metrics, and the ability to inspect the running system. The API is containerized or otherwise observable. You likely have multiple instances or a load balancer.</project>
  <task>You want a diagnostic framework — which questions to ask first, what signals matter, what to monitor — not a fix yet.</task>
  <operator>You're experienced enough to know 502s can come from dozens of places (app crash, resource exhaustion, downstream failure, load balancer timeout, network). You need to collapse the search space fast.</operator>
</assumptions>

### What I'm unsure of
- **Stack**: language, framework, runtime (Go, Node, Python, JVM?) — memory leaks, event loop blocking, and GC pauses manifest differently
- **Architecture**: is this a single service or does it call downstream APIs/databases? Where's the 502 originating (load balancer, reverse proxy, app itself)?
- **Observability**: do you have structured logs, APM (DataDog, New Relic), or metrics? Or mostly raw logs?
- **Deployment**: when did this start? Any recent changes (code, config, infrastructure, traffic pattern)?

### Diagnostic decision tree

The fastest path is to **separate upstream from downstream**, then **separate application from resource**. Here's the structure:

| Signal | What it tells you | Check first |
|---|---|---|
| **502 from load balancer logs** | LB can't reach backend, or backend closes connection | LB error logs, backend availability |
| **502 from reverse proxy / app logs** | App is crashing, timing out, or returning bad response | App error logs, restart frequency, memory/CPU at crash time |
| **Spike in response time *before* 502s** | Resource exhaustion or cascading slow requests | CPU, memory, goroutine/thread count, connection pool saturation, DB query time |
| **No app logs for a 502** | Process crash or hard kill | Check if instances are restarting, OOMKilled, or killed by orchestrator |
| **Regular interval (e.g., every hour on the hour)** | Scheduled job, cache expiry, load pattern, or monitoring probe | Cron jobs, cache TTL, traffic patterns, scheduled backups |
| **Hits one instance only** | Instance-specific issue (memory leak, stuck connection) | Logs per instance, memory growth over time |
| **Hits all instances simultaneously** | Downstream service down, network partition, or shared resource exhausted | Dependency health, database connection pool, shared cache |

### Three parallel tracks to start immediately

**Track 1: Narrow the origin** (5 min)
- Check your load balancer / ingress / reverse proxy logs for the exact 502s. Does the error originate there, or is it being forwarded from the app?
- Check app process logs *at the exact timestamp* of each 502. Are there errors, crashes, or just silence?
- If silence: the process may be crashing or being killed. Check orchestrator (Kubernetes, systemd, etc.) for restarts.

**Track 2: Correlate with resources** (10 min)
- Pull a 5-minute window around each 502 incident.
- Graph: CPU, memory, open file descriptors, connection count (database, HTTP), goroutine/thread count (language-specific).
- Look for a spike *just before* the 502, not after.
- If memory is growing steadily, you have a leak. If it spikes suddenly, you have a spike in request volume or a bug.

**Track 3: Check for periodicity** (5 min)
- Export the timestamps of all 502s from the last 24 hours.
- Plot them. Is there a pattern? (Every hour, every 10 minutes, clustering around certain times?)
- If yes: check cron jobs, scheduled tasks, traffic patterns, health checks, or batch operations.
- If no: move to application-level debugging.

### Recommended path
Start with **Track 1** and **Track 2 in parallel**. Track 1 answers "where is the 502 coming from?" Track 2 answers "what was the system state when it happened?" Together, they'll point you at either:
- **App crash / restart** → check logs, recent changes, resource limits
- **Timeout** → upstream or downstream slow? Check latency metrics
- **Resource exhaustion** → memory leak, connection pool, file descriptor limit
- **External dependency** → database down, cache down, downstream API down

Once you know which one, you'll have a specific thing to fix.

### Next prompt should include
- Which track you ran first and what you found (or which logs I should help you parse)
- Your stack (language, framework) and architecture (single service? calls downstream?)
- Whether you have metrics/APM or just raw logs
- When this started (same day as a deploy, or out of nowhere?)