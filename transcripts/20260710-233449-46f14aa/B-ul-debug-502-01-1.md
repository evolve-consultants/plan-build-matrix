**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You have a production API that returns 502 Bad Gateway errors roughly hourly with no obvious trigger. You need a systematic starting point for diagnosis — not solutions yet, but a framework for narrowing down the cause.

<assumptions>
  <project>You have logs (application, access, infrastructure), monitoring already in place, and some ability to correlate events. You've ruled out the obvious (recent deploys, sudden traffic spikes).</project>
  <task>You want to move from "it's broken sometimes" to "it's broken because X" so you can fix it deliberately.</task>
  <operator>You have production access and can pull logs/metrics. You're comfortable with infrastructure details but may not have deep visibility into every layer.</operator>
</assumptions>

### What I'm unsure of
- **Architecture**: Is this a monolith, microservices, serverless? Do you have a load balancer, reverse proxy, or multiple API instances?
- **Existing visibility**: What's your current logging/monitoring? (structured logs, APM, metrics platform?)
- **Reproducibility**: Can you trigger a 502 on demand, or does it only happen in production?
- **Blast radius**: Does the 502 affect all requests or a subset? (certain endpoints, certain users, certain request types?)

### The Diagnosis Framework

Start by **narrowing the layer** — 502 means "the proxy/load balancer got no response from the backend." That could be:

1. **Application tier**: Your code is crashing, hanging, or becoming unresponsive
2. **Connection tier**: Database, cache, external service timeouts or connection pool exhaustion
3. **Infrastructure tier**: Memory leak, file descriptor limit, network saturation, container restart
4. **Proxy tier**: Load balancer misconfiguration, health check failures, routing errors

Then **correlate timing** — find what else happened in the 5 minutes before each 502.

### Three immediate steps (highest leverage, no special tooling)

| Step | What it answers | How to do it |
|---|---|---|
| **1. Check restart logs** | Is the application crashing and restarting? | `kubectl logs <pod> --previous` (K8s) or check Docker/systemd logs. Look for exits, OOM kills, segfaults, unhandled exceptions. |
| **2. Correlate 502 timestamps to logs** | What's the application doing when 502s happen? | Pull your access logs (nginx/apache) and application logs. Find 502 entries, note exact timestamps, then grep your app logs ±30s around each one. What's the last thing logged before silence? |
| **3. Check resource exhaustion** | Is memory, CPU, or file descriptors saturated? | Pull CPU, memory, and open file descriptors over the last hour. Are there spikes at 502 time? (Prometheus, CloudWatch, whatever you use.) |

### Recommended path
**Start with Step 2** (log correlation) because it's fastest and often immediately reveals the cause (crash, exception, hang). If that's clean, move to Step 1 (restarts). If both are quiet, then Step 3 (resource metrics) usually pinpoints infrastructure issues.

Once you know *where* the failure is happening, we can drill into *why*.

### Next prompt should include
- Whether you've already checked any of these three
- Your architecture (monolith vs. services, containerized?)
- What logging/monitoring platform you have
- The results of whichever step you run first

What does your log timeline look like around a 502?