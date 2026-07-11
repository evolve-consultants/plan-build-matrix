**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You're experiencing performance issues in your app and suspect caching could help, but you don't have visibility into where the slowness is actually happening. You need a way to identify the real bottleneck before investing in a caching solution.

<assumptions>
  <project>You have a running app (web, mobile, backend — unclear which) with some kind of data access or computation layer</project>
  <task>You want to find the root cause of slowness and determine whether caching is the right fix</task>
  <operator>You're willing to add instrumentation but probably want a pragmatic approach, not days of profiling</operator>
</assumptions>

### What I'm unsure of
- **What kind of app**: web frontend, backend API, mobile, desktop?
- **When it's slow**: always, under load, specific user actions, intermittently?
- **What "slow" means**: takes 5 seconds when it should take 1? Spikes to 30s? Consistent baseline?
- **Current stack**: what language, framework, and data layer (database, API calls, file I/O)?
- **What you've already measured**: any monitoring, logs, or profiling data in place?

### Options

| | Upside | Downside | Best when |
|---|---|---|---|
| **A: Add logging + manual timing** | Fast to implement, reveals bottlenecks in your code, no dependencies | Requires redeploy, data only for instrumented paths, easy to miss network/DB time | You control the code and can iterate quickly; slowness is likely in your own logic |
| **B: Use built-in profiling tools** | Comprehensive (CPU, memory, I/O), finds hidden bottlenecks, no code changes needed | Overhead during profiling, can be overwhelming for complex apps, requires learning the tool | You need a full picture; you're willing to spend 1–2 hours analyzing output |
| **C: Add APM (Application Performance Monitoring)** | Traces entire request lifecycle (code → network → DB), real production data, ongoing visibility | Adds infrastructure cost, requires setup, can be overkill for small apps | You have production traffic and need ongoing monitoring, or slowness is inconsistent |
| **D: Profile the specific slow action** | Surgical, fast answers, confirms whether it's code or external (DB/network) | Only works if you can reproduce the slowness reliably | You can trigger the slow behavior on demand |

### Recommendation
**Start with Option A (logging + timing)** because:
- It's fastest to implement and fastest to get a result
- It immediately answers: "Is it my code, or something else (DB, network, external API)?"
- Once you have that answer, you'll know whether caching helps and *where* to apply it
- If logging shows the bottleneck is external (DB query takes 2s), you've already validated that caching would help
- If it's your own code looping or processing, you might not need caching — you might need optimization instead

Once you know where the time is going, we can design a caching strategy that fits.

### Next prompt should include
- **What kind of app** (web API? frontend? background job?)
- **When it's slow** (specific action, or general baseline, or under load?)
- **How slow** (actual numbers if you have them)
- Which option you want to start with, or confirmation that you'll try logging first

I can then give you the exact instrumentation code to add and walk you through interpreting the results.