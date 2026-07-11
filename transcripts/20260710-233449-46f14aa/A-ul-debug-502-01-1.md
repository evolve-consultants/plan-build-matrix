# Debugging Intermittent 502s

Start with these in parallel—don't assume it's what you think:

## Immediate signals to check

**Load patterns**
- Is it truly random, or correlated with time-of-day, deploys, traffic spikes, or specific endpoints?
- Pull metrics for the past week. Graph request rate + 502 rate together
- Check if it's all users or specific regions/clients

**Upstream dependencies**
- 502 usually means your server received a bad/no response from something it called
- Check logs for timeouts, connection resets, or errors from: database, cache, external APIs, load balancer
- Any of those timing out would cause 502s

**Server-side capacity**
- Memory leaks? Connection pool exhaustion? File descriptor limits?
- During a 502 incident: `ps aux`, `free -h`, `netstat -an | grep ESTABLISHED | wc -l`
- Check if you're hitting limits on your platform (AWS connection limits, container memory, etc.)

## Investigation approach

1. **Narrow the scope**: Is it one endpoint, one service, all traffic? Check access/error logs
2. **Capture the incident**: Set up alerts on 502 rate. When it happens next, immediately grab:
   - Full application logs (not just errors)
   - Dependency latency metrics
   - Resource usage (CPU, memory, connections)
3. **Check recent changes**: Deploys, config changes, dependency updates in the last 2 weeks?

## Most common culprits I've seen
- Database connection pool exhausted (slow queries cause pile-up)
- External API timeout making requests hang (timeout not set, or set too high)
- Memory leak in a worker process causing restarts
- Kubernetes resource limits being hit
- Gateway/load balancer misconfiguration (bad upstream health checks)

What's your stack, and do you have access to application logs + metrics dashboards?