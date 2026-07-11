**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You're getting sporadic 502s in production with no obvious trigger, and you need a systematic way to narrow down the cause — not a guess about what might be wrong, but a diagnostic framework.

<assumptions>
  <project>You have a web service with multiple instances, probably load-balanced. You have logs. You don't know yet if this is your code, infrastructure, dependencies, or downstream services.</project>
  <task>You want to reduce MTTR by building a diagnostic map: *which layer is actually failing* so you can hand it to the right team or start fixing the right thing.</task>
  <operator>You can access logs and metrics. You probably don't have infinite time to instrument everything. You want to move fast and eliminate categories of problems rather than shotgun fixes.</operator>
</assumptions>

### What I'm unsure of
- **Observability depth**: Do you have structured logging, APM (DataDog, New Relic, etc.), or just access logs? This changes what you can see.
- **Scale**: Is this a small service or a large distributed system? Single instance vs. fleet? Changes diagnostic strategy.
- **Recent changes**: Did this start after a deploy, infra change, or library upgrade? Or truly random onset?
- **Consistency**: Does it hit all instances equally, or is it clustered on certain boxes?

---

## Diagnostic Decision Tree

The fastest way forward is to **eliminate layers top-to-bottom**. A 502 from your load balancer is different than a 502 from your app.

### **Step 1: Is it actually your service returning 502, or is the LB/gateway returning it?**
- Check your **app logs** for requests during the 502 window. If they're not there, the LB is failing before it hits you.
- Check **LB/reverse proxy logs** (nginx, HAProxy, AWS ELB, etc.). Are requests reaching your app? Are they timing out?
- **Why this matters**: If the LB is returning 502 but your app isn't even seeing the request, you're looking at connection pools, DNS, or gateway timeouts — not your code.

### **Step 2: If it's your app, what's the common thread?**
- **Memory**: Is heap spiking right before 502s? Check garbage collection logs and heap usage graphs.
- **Connections**: Are you hitting connection pool limits (DB, cache, external APIs)? Check "waiting for connection" errors.
- **Latency**: Are requests hanging before returning 502? Correlate request duration with 502 timestamps.
- **Dependencies**: When a 502 occurs, what were the last downstream calls (database, cache, third-party API)? Did *they* fail or timeout?
- **Why this matters**: These point to resource exhaustion, blocking calls, or cascading failures — very different fixes.

### **Step 3: Is there a time-of-day, load, or request-type pattern?**
- Even "no pattern" often has one once you break it down:
  - Does it correlate with request volume (QPS spike)?
  - Does it correlate with specific endpoints or request types?
  - Does it correlate with time-of-day (database backup, batch job)?
  - Does it correlate with instance age (memory leak)?
- **Why this matters**: A leak that shows up after 4 hours of uptime is very different than a connection pool exhaustion on every 10,000th request.

---

## Instrumentation Priority (if you're not already logging this)

If you don't have structured logging or APM yet, instrument in this order:

1. **Request timing + dependency calls** (add a middleware/interceptor that logs: request start, each downstream call with duration, request end, response code)
2. **Resource metrics** (heap, connection pool counts, thread pool queue depth — these should be available in your runtime already)
3. **Error context** (when a 502 happens, log the full stack trace + last 5 requests + current resource state)

You don't need fancy observability to solve this. Structured logs with timestamps let you correlate 502s with resource metrics.

---

## Options for Next Step

| | Move | Upside | Downside | Best when |
|---|---|---|---|---|
| **A: Check logs first** | Pull app + LB logs from a 502 incident window. Find the exact request(s) and what they were doing. | Eliminates broad categories fast. Might solve it in 10 minutes. | Requires logs to exist and be queryable. | You haven't yet confirmed whether your app is even seeing the request. |
| **B: Add instrumentation** | Deploy middleware/interceptor that logs request timing, dependency calls, and resource state. Wait for next 502. | Gives you visibility into the actual failure mode for future incidents. Repeatable. | Takes time to deploy. Doesn't help with the current incident unless it's truly intermittent. | Logs aren't detailed enough to diagnose, or you need to solve this systematically for recurring issues. |
| **C: Profile under load** | Spin up a staging environment and load test the same traffic pattern. Try to reproduce the 502. | Might trigger the bug faster than waiting for production. | May not reproduce if it's timing-dependent or requires specific data state. | You suspect load or specific request types are involved. |

---

## Recommendation

**Start with Option A** (check logs) because:
- It's the fastest way to answer "is this my code at all?"
- It might solve the problem immediately (e.g., if downstream API is failing)
- Even if it doesn't pinpoint the cause, it narrows the problem space dramatically
- It costs nothing and takes 15–30 minutes

**Then move to Option B** if logs don't show the culprit — structured instrumentation will let you catch the next incident in a way that's actionable, not just a 502 timestamp.

### Next prompt should include
- Whether you have logs from a recent 502 (app + LB), and if so, what you found
- What observability you currently have (logs, metrics, APM?)
- Whether there's been a recent deploy or change before these started
- Rough scale (single instance? 10? 100?)

Once I have answers to those, I can walk you through parsing the logs or building the right instrumentation.