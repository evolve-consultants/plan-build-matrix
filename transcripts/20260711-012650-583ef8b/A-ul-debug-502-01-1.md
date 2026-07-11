# Debugging Intermittent 502s

Start by separating **what's actually failing** since 502s can come from multiple layers:

## 1. First: Verify it's actually your backend
- Are 502s coming from your load balancer/reverse proxy (nginx, HAProxy, ALB) or your application servers?
- Check access logs on the reverse proxy layer for timing/distribution
- A 502 there means either:
  - The backend didn't respond in time
  - The connection was closed unexpectedly
  - The backend was unreachable

**Quick test:** Add a simple health check endpoint that logs every hit. If LB is hitting it successfully during "502 windows," the problem is likely in request handling, not availability.

## 2. Check the obvious resource issues
```bash
# During a 502 window:
- Memory: Is anything approaching limits? Swap usage creeping up?
- Connections: netstat/ss - established count, TIME_WAIT buildup?
- CPU: Spikes or sustained high load?
- Disk I/O: Particularly if you log heavily
- Database connections: Are they exhausted?
```

Focus especially on **connection pool exhaustion**—often invisible in CPU/memory metrics but causes exactly this symptom.

## 3. Correlate with your logs
- Application error logs during 502 windows (stderr, exceptions)
- Slow query logs (DB queries hanging briefly?)
- Request latency percentiles (p95/p99 spiking?)

The 502 *itself* is a symptom. Look for what causes the backend to stop responding.

## 4. Common culprits for "once an hour" patterns
- **Scheduled jobs/cronjobs** (backups, cache invalidation, reports)
- **Database maintenance** (autovacuum, log rotation)
- **Periodic spikes** in upstream dependencies (another service, external API)
- **Connection pool exhaustion** from a slow downstream service

**Action:** Check your cron jobs, monitoring dashboards, and any scheduled tasks on dependent systems.

## 5. What to instrument **right now**
If you don't have this, add it immediately:
```
- Request duration histogram (milliseconds)
- Backend response time vs. proxy timeout
- Active connections to backend
- Error rate by endpoint
- Queue depth if you're using a task queue
```

**What's your stack?** (language, framework, reverse proxy?) The next steps differ significantly between e.g. Node single-threaded vs. Go concurrent vs. a Python app with limited workers.