**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You have a production API that returns 502 Bad Gateway errors roughly once per hour with no obvious triggering pattern, and you need a systematic approach to narrow down the root cause.

<assumptions>
  <project>You have access to logs, monitoring, and the ability to inspect production behavior. I'm assuming this is a web service (not embedded), running on standard infrastructure (cloud or on-prem with observability). I don't know the tech stack, scale, or whether you're running a monolith or distributed system.</project>
  <task>You need to move from "502s happen randomly" to "502s happen when X does Y" — narrowing the hypothesis space so you can fix it, not just suppress alerts.</task>
  <operator>You have SRE/DevOps/engineering chops to SSH into servers, read logs, and run queries. You probably don't have unlimited time to debug. You want the next concrete step, not a framework lecture.</operator>
</assumptions>

### What I'm unsure of
- **Tech stack & architecture**: Language? Load balancer (nginx, HAProxy, cloud LB)? App server behind it? Reverse proxy chain? Database? External dependencies?
- **Observability**: What do you currently monitor? Do you have structured logs? APM (DataDog, New Relic, etc.)? Do you see 502s in app logs or only at the load balancer?
- **Scale & traffic patterns**: How many requests/sec? Is traffic steady or bursty? Any scheduled jobs or batch processes running hourly?
- **Recent changes**: Deploys, config changes, dependency updates in the last week or two?

### High-level strategy
502s happen at a specific layer. Your job is to find it:

1. **Confirm the layer** (LB vs. app vs. external dependency)
2. **Correlate with system state** (memory, CPU, connections, queue depth at moment of failure)
3. **Narrow the trigger** (specific endpoint? request type? load condition?)
4. **Reproduce** (once you can trigger it consistently, fix follows)

### Options for your next move

| | Upside | Downside | Best when |
|---|---|---|---|
| **A: Load balancer logs + app logs side-by-side** | Immediately tells you if the problem is upstream (LB/ingress) or downstream (your app can't respond). Cuts hypothesis space in half. | Requires access to both; if your LB isn't logging requests, you waste time. | You haven't yet confirmed *where* in the stack the 502 originates. START HERE unless you already know. |
| **B: System metrics at the moment of 502** | Memory spikes, CPU saturation, connection pool exhaustion, and queue buildup are common culprits. A 502 correlating with resource exhaustion points you straight at "why can't the app respond?" | Requires you to correlate timestamps accurately and have 1-hour retention on detailed metrics. Noisy if you don't filter by 502 events. | You suspect resource limits or saturation (memory leaks, connection leaks, thundering herd). |
| **C: Request-level tracing / APM** | If you have DataDog, New Relic, or similar, you can see exactly which requests succeeded/failed around the 502 and what they were doing. Bypasses guesswork. | Expensive and requires setup if you don't have it. Overkill if you can solve it faster. | You suspect a specific endpoint or request type triggers it, or you already have APM running. |
| **D: Reproduce in staging** | Once you have a hypothesis (e.g., "502 happens under high memory pressure"), you can test it safely. | Staging != production; load patterns, data volume, and concurrency often differ. May not reproduce. | You have a specific hypothesis to test and need confirmation before deploying a fix. |

### Recommendation
**Start with Option A** — load balancer and app logs side-by-side, filtered to the exact timestamps of 502 errors.

**Why:** A 502 means the load balancer received a request but the upstream app server didn't respond in time (or closed the connection). The LB logs will tell you:
- Did the request reach your app at all?
- How long did the LB wait before timing out?
- Were multiple 502s happening at once, or isolated?

The app logs will tell you:
- Was your app even running?
- Do you see errors around that time?
- Was it handling requests normally, or frozen / crashing?

If LB saw the request but the app logs show nothing, you've narrowed it to app-level (process crash, hang, or silent failure). If the LB logs are empty but your app was fine, something upstream is rejecting requests.

### Next prompt should include
1. **What you find in the logs**: Show me a 502 event with timestamps from both LB and app. Even a sanitized excerpt helps.
2. **Stack specifics** if you want me to help interpret what you find: language, LB type, app server (Gunicorn, Puma, Tomcat, etc.), any reverse proxy between them.
3. **Whether you already have APM or detailed system metrics** — if yes, that's our Option B path instead.