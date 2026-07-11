**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You've noticed performance problems in your app and suspect caching could help, but you don't know where the bottlenecks actually are. You want a strategy for finding and fixing them.

<assumptions>
  <project>I'm assuming you have a web or mobile app with backend components, but I don't know the tech stack, scale (users/requests/data), or architecture</project>
  <task>You want to improve perceived performance, but I'm unsure whether "slow" means occasional spikes, consistent baseline slowness, or specific features that drag</task>
  <operator>I'm assuming you have access to logs/metrics and can deploy changes, but I don't know your monitoring capability or risk tolerance for adding infrastructure</operator>
</assumptions>

### What I'm unsure of
- **Tech stack**: Is this a React/Node app, Rails, Django, native mobile, or something else? (Changes where caching happens)
- **What's slow**: Are specific pages/endpoints sluggish, or does the whole app feel unresponsive? Is it backend latency or frontend rendering?
- **Scale**: How many concurrent users? How much data are you moving?
- **Current visibility**: Do you have any performance metrics, logs, or profiling tools in place already?
- **Caching layer**: Are you thinking HTTP caching, database query caching, in-memory caching (Redis), or API response caching?

### Options

| | **Approach** | **Effort** | **Best when** |
|---|---|---|---|
| **A** | Profile first, cache second | 4–8 hours | You don't know where time is spent; you need data before buying infrastructure |
| **B** | Add a caching layer (Redis/Memcached) immediately | 2–4 hours | You're confident the bottleneck is repeated database queries or API calls |
| **C** | Instrument the app with metrics first | 6–12 hours | You want long-term visibility into performance; this pays dividends over months |
| **D** | Quick wins: optimize obvious queries, add database indexes | 2–4 hours | You suspect N+1 queries or missing indexes but haven't confirmed |

### Recommendation
**Start with A (Profile first)** because caching is a tool for a *specific* problem, not a cure-all. If you cache the wrong thing, you'll spend time and infrastructure cost on zero benefit. Profiling takes a few hours, gives you certainty, and often surfaces low-hanging fruit (missing indexes, bad queries) that don't require caching at all.

After profiling, you'll know whether your real bottleneck is database, API calls, or rendering—and *then* you can pick the right caching strategy.

### Next prompt should include
- **Your tech stack** (frontend and backend)
- **What "slow" looks like** (always slow? intermittent? specific features?)
- **Whether you have monitoring/profiling tools** already (or want help setting them up)
- **If you want to start with profiling or jump to adding Redis**

Once I know these, I can give you the exact steps to run.