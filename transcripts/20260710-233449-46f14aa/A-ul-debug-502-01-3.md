# Systematic 502 Troubleshooting

Start by separating **where** it happens from **why**:

## Immediate data collection (before it happens again)

1. **Capture the exact context**
   - Enable verbose logging on requests *around* 502s (5 min before/after)
   - Log: request size, headers, response time, which backend server responded
   - Check if 502s cluster or are truly random
   - Note: time of day, traffic volume, deployments, cron jobs

2. **Check infrastructure layers** (in parallel, ~15 min)
   ```
   - Load balancer logs/metrics (connection resets? timeouts?)
   - Your app servers (crashes, restarts, resource spikes?)
   - Database (connection pool exhaustion? slow queries?)
   - Any reverse proxy/middleware between client and app
   ```

3. **Look for the "smoking gun" pattern**
   - Same backend server? → server-specific issue
   - Correlated with traffic spike? → capacity/connection limit
   - Correlated with a specific endpoint? → code issue
   - Random across all servers? → external dependency

## Most common culprits (statistically)

- **Database connection pool exhaustion** (bleeds into production slowly)
- **Backend process crash/restart** (check error logs, OOM killer)
- **Upstream timeout** (load balancer/reverse proxy timeout too short)
- **Memory leak** (restarts once an hour via watchdog?)
- **Hung requests** (blocking operation not timing out)

## Quick wins to try

```
- Increase connection pool limits (if you haven't tuned them)
- Lower timeouts on slow operations (fail fast instead of hanging)
- Add health check endpoint that actually tests dependencies
- Increase backend worker/thread count
```

**What specific stack are you running?** (language, framework, load balancer) That'll narrow down where to look first.