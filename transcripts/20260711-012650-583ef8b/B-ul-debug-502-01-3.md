**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You have an API that's returning 502 Bad Gateway errors roughly once per hour with no obvious trigger, and you need a systematic approach to diagnose the root cause.

<assumptions>
  <project>This is a web service with load balancers/reverse proxies in front (hence 502s, which come from upstream failures). You have logs available. The issue is recent or newly noticed.</project>
  <task>You want to move from "we don't know what's happening" to "here's what's broken" in a way that doesn't require days of speculation.</task>
  <operator>You have access to logs, metrics, and can deploy/restart if needed. You probably own the app layer but may not own infrastructure.</operator>
</assumptions>

### What I'm unsure of
- **Error surface**: Are 502s from your app crashing, timing out, responding slowly, or something else? (Different root causes live in different places.)
- **Scale/load**: Is this a small service or high-traffic? Does it happen during peak times?
- **Stack**: What's the app (language, framework)? What's in front (nginx, HAProxy, AWS ALB)?
- **Observability**: Do you have structured logs, APM (New Relic, DataDog, etc.), or just access logs?
- **Recent changes**: Deploy, config change, dependency update, or database change in the last week?

### Three diagnostic paths, ranked by speed-to-insight

| | What you'll find | Effort | Best when |
|---|---|---|---|
| **A: Access logs first** | Whether the app is even responding (502 from load balancer vs. from app) | 5 min | You need a quick signal right now |
| **B: Correlate metrics** | CPU, memory, GC pauses, DB connection exhaustion, queue buildup | 15–30 min | You have metrics/APM available |
| **C: Reproduce locally** | Whether it's environmental or code-based | 30 min–2 hrs | Everything else points to the app |

### Recommendation
**Start with A (access logs).** A 502 tells you *where* it failed — if the load balancer is getting no response from your app within the timeout window, you'll see `502` alongside missing or slow access log entries. That single fact collapses half the problem space.

If logs show the app *is* responding but slow/timing out → move to B (metrics). If logs show the app isn't responding at all → look for crashes/hangs in application logs and jump to C.

### Next prompt should include
- **Access logs from a 502 incident**: Show me 30 seconds before, during, and after one error
- **Your stack**: language, framework, what sits in front
- **Whether you have metrics/APM**: and if so, what's available
- **Any recent changes**: deploys, config, dependencies, database migrations

Once I see logs + stack, I can give you the exact grep/metric queries to run and where to look next.