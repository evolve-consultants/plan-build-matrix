# Debugging Intermittent 502s

Start with these high-signal investigations:

## Immediate: Check upstream dependencies
- **Database connections**: Are you hitting connection pool limits? Monitor active/idle connections when 502s occur
- **External APIs**: Are timeouts happening? Check if those services have issues around the 502 timestamps
- **Load balancer/reverse proxy logs**: The 502 source (nginx, HAProxy, etc.) usually logs *why* it rejected the connection — this is often more useful than app logs

## Next: Correlate with metrics
Pull data for the exact times 502s occurred:
- **Memory**: Sudden spikes, GC pauses, memory leaks?
- **CPU**: Saturation or context switching?
- **Request latency**: Are requests just slow (causing timeouts) rather than actually failing?
- **Concurrent request count**: Hitting a limit?

## Then: Application-level
- **Worker/thread exhaustion**: If using gunicorn, uWSGI, etc., are workers hanging on slow operations?
- **Slow queries**: One query locking resources? Check slow query logs
- **Cascading timeouts**: Service A times out waiting for B, which times out waiting for C

## The practical shortcut
If you have any APM (Datadog, New Relic, etc.): **filter to transactions ending in 502** and look at what's different about them vs successful requests.

**What's your stack?** (language, web framework, deployment environment) — that narrows down the most likely culprits significantly.