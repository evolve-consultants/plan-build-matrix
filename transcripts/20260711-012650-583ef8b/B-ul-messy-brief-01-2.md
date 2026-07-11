**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You've noticed performance degradation in your app at times, suspect caching could help, but you don't have a clear diagnosis of what's actually slow. You want to know how to approach the problem.

<assumptions>
  <project>I'm assuming this is a web/mobile app with a backend, but I don't know the tech stack, scale, or architecture.</project>
  <task>I'm assuming you want to fix real performance issues (not premature optimization), and you're open to discovering the root cause rather than jumping straight to caching.</task>
  <operator>I'm assuming you have access to the running app and logs/metrics, but I'm unsure about your monitoring visibility or debugging experience.</operator>
</assumptions>

### What I'm unsure of
- **What "slow sometimes" means**: Is it page load time, API response time, database queries, rendering, or something else? Is it slow for all users or just some?
- **Tech stack**: Frontend framework, backend language/framework, database, hosting environment?
- **Current visibility**: Do you have logs, APM (Application Performance Monitoring), or browser dev tools data, or are you flying blind?
- **Scale**: Is this a high-traffic app or a smaller one? Are there known spikes?
- **What you've already tried**: Any instrumentation, profiling, or performance work done before?

### Options

| | Approach | Upside | Downside | Best when |
|---|---|---|---|---|
| **A: Measure first** | Use browser dev tools, server logs, or APM to identify the actual bottleneck before caching | You'll fix the real problem, not guess. Might reveal the issue isn't cacheable. | Takes time upfront; requires some instrumentation skill | You have no data yet and want to avoid wasting effort on the wrong thing |
| **B: Profile common flows** | Trace a few user journeys (page load, API call, etc.) to see where time is spent | Quick, concrete, actionable without heavy tooling | Might miss edge cases or slow queries that only happen sometimes | You have a hunch about what's slow but no proof |
| **C: Add caching speculatively** | Cache the most likely culprits (API responses, database queries, expensive computations) and measure impact | Fast to implement if you know what to cache; gives immediate confidence | You might cache the wrong thing and waste time; won't help if the problem is elsewhere | You have strong confidence about the bottleneck already |
| **D: Set up proper monitoring** | Instrument with APM (e.g., New Relic, DataDog, Sentry) or logging to get continuous visibility | You'll see the problem as it happens; catches regressions automatically | Setup and cost; overkill if this is a one-off investigation | You need ongoing visibility or this is a recurring mystery |

### Recommendation
**Start with A (Measure first)**, then move to B (Profile common flows) if you don't find the answer immediately. Here's why:

- Caching can help, but it's often not the bottleneck. You might cache something that's already fast while the real culprit goes unfixed.
- Measurement takes 15–30 minutes and gives you concrete direction.
- Once you know the problem, the caching decision becomes obvious.

### Next prompt should include
- **Tech stack** (frontend framework, backend, database)
- **How "slow" manifests** (e.g., "page takes 5 seconds to load" or "API calls stall for 10 seconds randomly")
- **Whether you have any monitoring in place** (even just browser dev tools)
- **Which user flows are slowest** (if you have a hunch)

Once I know these, I can walk you through the exact steps to diagnose the problem.