**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You're getting occasional 502 Gateway Bad Gateway errors in production with no obvious trigger, and you need a diagnostic framework — where to look first, what to measure, how to narrow it down.

<assumptions>
  <project>You have a web API behind a load balancer or reverse proxy (nginx, AWS ALB, etc.). Backend services exist (app servers, databases, caches). You have some observability in place (logs, metrics) but maybe not comprehensive traces.</project>
  <task>You want to stabilize the service by finding whether the issue lives in load balancing, application code, dependencies, or infrastructure — and what to check first.</task>
  <operator>You can access logs/metrics, restart services, and coordinate with your team on investigation. You want a systematic path, not random debugging.</operator>
</assumptions>

### What I'm unsure of
- **Stack**: Is this Node/Python/Go/Java? Docker + K8s, or VMs, or serverless?
- **Load balancer**: What's in front (nginx, ALB, Cloudflare, custom)?
- **Current observability**: Do you have request logs, response times, error traces, or just "502 happened"?
- **Frequency signal**: Once an hour — is that tied to cron jobs, batch work, spikes, or truly random?
- **Scale**: Single instance, 5 instances, 100 instances?

### The Diagnostic Path (recommended)

A 502 means the reverse proxy *received* a request but couldn't get a valid response from the backend. The backend either:
1. Crashed or is unreachable
2. Didn't respond in time (timeout)
3. Returned an invalid/malformed response
4. Closed the connection unexpectedly

**Start here, in order:**

| Step | What to check | Why first | What you'll see |
|---|---|---|---|
| **1. Load balancer logs** | 502 errors in LB access logs. Check *which backend* served each 502, response time, connection state. | 502s are issued by the LB, not the backend. The LB logs tell you if it's a timeout, refused connection, or backend crash. | `upstream timed out`, `no live upstreams`, `502 Service Unavailable from backend-3` |
| **2. Backend logs at that timestamp** | App logs from the specific backend that returned 502. Errors, panics, OOMs, exceptions during the window. | If the backend crashed or threw an error, it's captured here. Correlate by timestamp. | Null pointer exception, out of memory, segfault, or silence (hung process) |
| **3. Infrastructure metrics** | CPU, memory, disk, network on both LB and backend instances during the 502 window. | Resource exhaustion causes hangs, timeouts, and crashes. | Spike to 100% CPU or memory, full disk, network saturation |
| **4. Dependency health** | Database connection pool, cache (Redis/Memcached), external service calls. Response times, error rates, connection count. | Timeouts to dependencies cause the app to hang, which triggers LB timeout → 502. | Spike in DB connection wait, Redis timeouts, or external API latency |
| **5. Application traces/profiling** | If you have APM (Datadog, New Relic, Honeycomb): trace a 502 request all the way through. See where it gets stuck. | Pinpoints which code path or dependency is hanging. | Trace shows request stuck waiting on DB query, lock contention, or external HTTP call |

### What to collect *right now* (before next occurrence)

So you don't have to scramble when the next 502 hits:

```
1. Load balancer config: What's the timeout setting? (default often 30s)
2. Backend error logs: Set to DEBUG or TRACE for the next few hours
3. Infrastructure dashboards: Set up CPU/memory graphs for the affected instances
4. Dependencies: Instrument slow queries, cache misses, external API calls
5. Request context: Add request IDs to logs so you can trace one 502 end-to-end
```

### Recommended path

Start with **load balancer logs** (step 1). That answer immediately tells you:
- Is it a timeout? (backend slow/stuck)
- Is it a connection refused? (backend crashed)
- Is it from one backend repeatedly, or different ones? (instance-specific vs. systematic)

Once you know *that*, you'll know whether to dig into app code (crash), infrastructure (resource), or dependencies (timeout).

### Next prompt should include

1. **Stack and infra**: What's your app built in? What's the load balancer?
2. **LB timeout**: What's the timeout setting currently?
3. **Observable pattern**: Is it always the same backend(s), or random? Any correlation with traffic spikes, deployments, or time of day?
4. **Observability**: Do you have centralized logging, APM, or just local logs?

Once I know those, I can walk you through the actual log queries or metric checks to run.