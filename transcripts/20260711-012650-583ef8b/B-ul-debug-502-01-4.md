**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
Your production API is returning 502 Bad Gateway errors roughly once per hour with no obvious trigger. You need a diagnostic starting point — not a fix yet, but a framework for where to look first.

<assumptions>
  <project>You have a traditional service architecture (probably load-balanced web servers or containers). You have some observability in place but may not have comprehensive tracing or request-level logging. The API handles meaningful traffic (enough to trigger issues reliably but not so much that noise drowns the signal).</project>
  <task>You want to narrow the scope: is this upstream (load balancer, reverse proxy), in-process (app crash, resource exhaustion), or downstream (database, external service timeout)? Once you know the layer, you can instrument and fix.</task>
  <operator>You're probably not in deep ops debt — you can pull logs and check basic metrics quickly. You're looking for a systematic approach, not a lucky guess.</operator>
</assumptions>

### What I'm unsure of
- **Which layer owns the 502?** Is it returned by your LB/reverse proxy (suggests backend timeout or crash), or by your app itself (suggests it's delegating the error up)?
- **Scale and traffic pattern.** Is this 100 RPS or 10k RPS? Does the error spike correlate with traffic spikes, or truly random?
- **Observability depth.** Do you have access to request logs, application metrics, container/OS metrics, and database slow query logs — or just HTTP access logs?
- **Recent changes.** Did this start after a deployment, a load increase, or infrastructure change, or was it always there?

### Options

| | Approach | Upside | Downside | Best when |
|---|---|---|---|---|
| **A: Upstream first** | Check if LB/proxy returns 502 or if app does. Check LB error logs, backend health checks, connection pool exhaustion. | Quick to rule out. Narrows scope fast. | Might be red herring if app is actually crashing. | You have clear LB logs and can compare 502 timestamps to backend state changes. |
| **B: Downstream first** | Assume app is timing out on DB/external service. Check connection pool sizes, query times, external service latency and error rates. | Catches the most common culprit (resource contention). | Takes longer to instrument if you lack query logs. | You know app is running but suspect I/O stalls. |
| **C: In-process first** | Assume app crashes or OOMs. Check app logs, memory usage, CPU, process restarts, exception rates at 502 timestamps. | Definitive if it's a crash — easy to see. | App might restart gracefully without logging the root cause. | You suspect an exception or memory leak. |
| **D: Systematic + parallel** | Instrument all three layers simultaneously: LB health check logs, app request logs + exceptions + resource metrics, database query times. Correlate by timestamp. | Finds the real culprit fast. Rules out multiple theories at once. | Requires more setup time upfront. | You have time to set up proper correlation and want to avoid ping-ponging between layers. |

### Recommendation
**Start with Option D (systematic + parallel), but execute it in phases so you're not building forever.**

Phase 1 (30 min): Collect baseline data from all three layers at the same timestamps as the next 502. Don't try to fix yet — just get signal. Phase 2 (1–2 hours): Correlate. Phase 3: Fix the layer that correlates.

Why this is best: A 502 that occurs "maybe once an hour" with no visible pattern will waste enormous time if you guess wrong and instrument in serial. Parallel collection converges faster and you get evidence instead of speculation.

### Next prompt should include
- Answers to the four uncertainties above (especially: does the 502 come from your LB or your app?)
- What observability tools you have (logs, metrics platform, APM, etc.)
- Recent changes or known traffic spikes
- Whether you want me to walk you through Phase 1 instrumentation, or you'd rather start with one specific layer