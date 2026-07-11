**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You've noticed performance dips in your app and suspect caching could help, but you don't have a clear diagnosis yet. You want a path to identify the actual bottleneck before investing in a solution.

<assumptions>
  <project>You have a running app (web, mobile, backend — unclear which), likely with some user-facing latency you've noticed anecdotally</project>
  <task>You want to improve performance, and caching seems like an obvious lever, but you're uncertain whether it's the right one</task>
  <operator>You may not have profiling tools set up yet, or you're not sure how to interpret their output</operator>
</assumptions>

### What I'm unsure of
- **What "slow" looks like**: Is it page load time? API response time? Specific features? Consistent or intermittent?
- **Your tech stack**: Web frontend, backend service, mobile app, database-heavy? This changes where bottlenecks typically hide.
- **What you've already measured**: Do you have any logs, timing data, or user complaints pointing to specific operations?
- **Your constraints**: Are you optimizing for user experience, server cost, or both?

### Options

| | Upside | Downside | Best when |
|---|---|---|---|
| **A: Measure first, then cache** | You'll find the *actual* problem before wasting time on the wrong solution. Avoids premature optimization. | Takes a bit longer upfront; requires tools or code changes. | You have time to do this right and want confidence you're solving the real problem. |
| **B: Cache the obvious things** | Quick wins; caching is rarely a mistake for expensive operations. Gets you moving. | You might cache something that isn't actually slow, missing bigger wins. | You have limited time or need to ship something now, and you're willing to iterate. |
| **C: Hybrid — measure one thing, then cache** | Finds a real bottleneck fast without full instrumentation. Pragmatic middle ground. | Only solves one problem per cycle; might miss multiple bottlenecks. | You have some sense of where slowness occurs but want proof before acting. |

### Recommendation
**Option A** (measure first). Here's why:

Caching is powerful but can hide bigger problems — slow queries, N+1 loops, unoptimized algorithms. If you cache the wrong thing, you'll feel productive but the slowness returns under different load. A quick profiling pass (15–30 minutes) will show you what's actually expensive and give you confidence that caching addresses the real issue.

**Next prompt should include:**
1. What type of app (web frontend, backend, mobile, etc.)
2. Where you notice slowness most (page load, specific features, API calls)
3. Whether it's consistent or happens under certain conditions (high traffic, large datasets, etc.)
4. Whether you already have any logging or monitoring in place

Once I know these, I can give you the exact profiling steps for your stack.