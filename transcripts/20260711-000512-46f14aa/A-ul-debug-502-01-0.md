# Debugging Intermittent 502s

Once-an-hour with "no pattern" usually means there *is* a pattern, you just haven't sliced the data the right way yet. Here's a systematic approach:

## 1. First, clarify what's actually returning the 502

502 = Bad Gateway, which means the error is coming from a proxy/load balancer, not your application directly. Identify every hop in the chain:

```
Client → CDN → LB/Reverse Proxy (nginx/ALB/etc) → App Server → (maybe another proxy) → Backend
```

The 502 could originate at any layer that sits in front of your actual app. Check logs at **each hop**, not just the app.

## 2. Pull the actual failed requests, not aggregates

Get the raw log lines for 5-10 actual 502 occurrences and look at:
- Exact timestamp (down to the second)
- Request path/method
- Upstream response time vs total time
- Which upstream/backend instance handled it
- Request size / response size

## 3. Look for correlation across these dimensions

- **Time-based**: Do they cluster at specific minutes (e.g., always :00 or :30)? → cron jobs, scheduled tasks, cache expiry
- **Instance-based**: Same backend server every time? → that instance has a problem (memory leak, restart, bad health check)
- **Load-based**: Does it correlate with traffic spikes or, conversely, quiet periods? → autoscaling, connection pool exhaustion, idle timeout
- **Endpoint-based**: Same route every time? → slow query, N+1, external dependency
- **Deploy-based**: Correlate with deploy times or rolling restarts

## 4. Common causes worth checking first (in likely order)

1. **Idle connection timeouts** — LB/proxy closes idle keepalive connections but backend (or vice versa) doesn't know yet, sends request into a dead connection. Check if timeout mismatch exists between LB and app server (e.g., ALB idle timeout vs nginx `keepalive_timeout`).
2. **Backend restarts/deploys** — health check briefly fails during rolling deploys or autoscaling events.
3. **Connection pool exhaustion** — app runs out of DB/upstream connections under specific load, hangs, LB times out waiting and returns 502.
4. **GC pauses / thread pool starvation** — app briefly unresponsive.
5. **Upstream dependency timeout** — a downstream service (auth, payments, etc.) occasionally hangs, and your gateway kills the connection before your app does.
6. **DNS resolution hiccups** — if backend addresses are resolved dynamically (K8s, ECS), stale DNS entries.

## 5. Quick wins to get more signal

- **Increase logging verbosity at the proxy layer** — nginx `error_log` at `warn`, ALB access logs with all fields enabled.
- **Log request duration for every request**, not just errors — helps you see if 502s correlate with slow requests.
- **Add a health-check / synthetic canary** hitting the same path every 10-30s so you get a denser sample of failures to correlate.
- **Correlate with infra events**: autoscaling activity, deploy timestamps, DB slow query logs, GC logs — line them up on one timeline.

---

**To help narrow this down further, can you tell me:**
1. What's in front of your app — nginx, ALB, Cloudflare, Kubernetes ingress, something else?
2. What's the app runtime (Node, Java, Python, Go, etc.)?
3. Do you have access to logs at both the proxy and app layer for the same request (i.e., can you correlate by request ID)?

That'll help me point you at the most likely culprit rather than a full checklist.