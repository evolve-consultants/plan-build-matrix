**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You're experiencing performance issues in your app and suspect caching could help, but you need a way to identify *where* the slowness actually is before implementing a solution.

<assumptions>
  <project>You have a working app (web, mobile, or backend — not yet specified). You can measure or observe the slowness but haven't profiled it yet.</project>
  <task>You want to identify bottlenecks systematically so you know whether caching is the right fix and where to apply it.</task>
  <operator>You're looking for a diagnostic approach, not a caching implementation yet. You probably have some ability to run profiling tools or monitor your app.</operator>
</assumptions>

### What I'm unsure of
- **App type**: Is this a web frontend, backend service, mobile app, or multiple layers?
- **How you're experiencing slowness**: Are specific user actions slow, or is the whole app sluggish? Do you see it in development, production, or both?
- **Scope**: Do you suspect slow API calls, heavy computation, rendering, database queries, or something else?
- **Instrumentation**: What monitoring or profiling tools do you already have access to?

### Options

| | Upside | Downside | Best when |
|---|---|---|---|
| **A: Start with browser/app profiling** | Identifies where *your* code is spending time. Very concrete — you'll see function calls, render cycles, or network waterfalls. Low overhead to start. | Requires you to trigger the slowness in a profiling session. Won't catch intermittent production issues. | Your app is a web frontend or mobile app, or slowness is reproducible locally. |
| **B: Add logging/instrumentation first** | Catches real production slowness. Gives you a picture of what users are actually experiencing. | Slower to iterate — you're waiting for production data. Requires log aggregation setup if you don't have it. | Slowness is intermittent or only happens in production under load. |
| **C: Profile the backend (API/database)** | If the bottleneck is server-side, you'll find it quickly. Caching decisions should be based on this data anyway. | If the problem is frontend, you'll waste time here. | You suspect slow API responses or database queries, or this is a backend-heavy app. |

### Recommendation
**Start with Option A** — profile what you can reproduce locally.

**Why**: It's the fastest way to get concrete data about where time is going. Even if production behaves differently, profiling your own code gives you a baseline and rules out obvious issues. If profiling shows everything is fast locally, you know the problem is either load-related (caching might help) or environment-specific (network, infrastructure).

Once you have that data, you can decide whether to add production instrumentation (Option B) or dig into the backend (Option C).

### Next prompt should include
- **App type** (web frontend, backend, mobile, or polyrepo?)
- **How to trigger the slowness** (specific user action, data size, or condition?)
- **Which tool you'd prefer to use** (browser DevTools, profiler, APM tool?)
- Or: which of the three options above matches your situation best