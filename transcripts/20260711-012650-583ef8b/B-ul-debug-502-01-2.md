**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You have a production API returning 502 Bad Gateway errors roughly once per hour with no obvious trigger, and you need a systematic way to narrow down the cause before diving into logs.

<assumptions>
  <project>You have observability in place (logs, metrics, APM) but haven't yet connected the 502s to a root cause. You own the API (not debugging a third-party dependency's infrastructure).</project>
  <task>You want a diagnostic framework to triage quickly — to know whether to look at code, infrastructure, dependencies, or client behavior first.</task>
  <operator>You have access to production logs and can likely reproduce the issue or at least observe it as it happens. You're looking for the next move, not a full postmortem.</operator>
</assumptions>

### What I'm unsure of
- **Are 502s coming from your load balancer/reverse proxy, or from your application itself?** (This splits the investigation in half.)
- **What's the traffic pattern?** (Steady, spiky, specific times of day?)
- **Do you have any APM or error tracking already?** (Datadog, New Relic, Sentry, etc.)
- **What's your stack?** (Node, Python, Go, Java, etc. — affects where to look first.)

### Three diagnostic paths

| | Approach | What it tells you | Cost |
|---|---|---|---|
| **A: Infrastructure first** | Check load balancer/reverse proxy logs and upstream health checks. Look for connection timeouts, backend pool exhaustion, or upstream service failures. | Whether your application is even receiving the requests, or dying before that. | 15 min, high signal |
| **B: Application behavior first** | Instrument the exact moment the 502 occurs in your app logs. Capture request ID, route, latency, and any exceptions. Correlate timing with traffic spikes. | Whether your app is crashing, hanging, or returning errors that the proxy is converting to 502. | 30 min, very high signal |
| **C: Dependency behavior** | Check response times and error rates from external services your API calls (databases, caches, third-party APIs). Look for timeouts or cascading failures. | Whether a slow or failing downstream service is causing your app to time out. | 20 min, medium-high signal |

### Recommendation
**Start with A (infrastructure logs).** Why: 502s are most often a symptom of either:
1. Your application crashing/restarting (load balancer can't reach it)
2. Your application taking too long (connection timeout)

A five-minute look at your load balancer logs will immediately answer *which* — and that answer determines everything downstream. If your LB can reach your app and is receiving responses, you skip straight to B. If it can't, you either have a crash or saturation problem.

### Next prompt should include
- What you find in your load balancer logs during one of these incidents (error codes, latency, connection counts)
- Answers to the three uncertainties above, especially stack and whether you have APM
- Whether the 502s are consistently returning within a few seconds or taking longer

If you give me those, I can write a targeted instrumentation plan or tell you exactly which logs to pull.