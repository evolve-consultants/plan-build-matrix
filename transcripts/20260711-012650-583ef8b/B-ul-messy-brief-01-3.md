**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You've noticed performance dips in your app and suspect caching could help, but you don't have a clear diagnosis yet. You want guidance on how to find the actual bottleneck before implementing a solution.

<assumptions>
  <project>You have a working app (web, mobile, backend — unclear which). You can observe slowness but don't have profiling data yet.</project>
  <task>You want a systematic way to identify what's slow, confirm caching is the right fix, and know where to apply it.</task>
  <operator>You're pragmatic about adding tools/instrumentation. You'd rather solve the right problem than guess and iterate.</operator>
</assumptions>

### What I'm unsure of
- **What kind of app**: web frontend, backend API, mobile app, full stack?
- **When it's slow**: on first load, during specific user actions, under load, intermittently?
- **What slow means**: milliseconds, seconds? Is it noticeable lag or full-page hangs?
- **What data/compute happens**: are you fetching from a database, external API, doing heavy calculation, rendering complex UI?
- **Your current stack**: what language/framework? Any instrumentation already in place?

### Options

| | Upside | Downside | Best when |
|---|---|---|---|
| **A: Profile first, then cache** | Finds the real bottleneck. Avoids premature optimization. Caching is targeted and effective. | Takes time upfront. Requires instrumentation. | You're willing to spend an hour diagnosing before coding. You want confidence that caching will actually help. |
| **B: Add caching to likely spots** | Fast to implement. Might solve it immediately. Low risk if caching layer is simple. | Might cache the wrong thing. Wastes effort. Hides the real problem. | You've done this before and know where slowness usually hides in your stack. You're confident about the architecture. |
| **C: Hybrid — quick profile + targeted cache** | Balances speed and accuracy. Light instrumentation (browser DevTools, app logs, simple metrics). | Still requires some setup. Might miss non-obvious bottlenecks. | You want to move fast but have some data. You can add logging in 10 minutes. |

### Recommendation
**Option C (Hybrid)** — you get quick signal without heavy upfront work.

Here's why: even a 15-minute profile will show you whether the slowness is in the network, database, rendering, or computation. That single fact eliminates guessing. Caching is great, but it's a solution to *specific* problems (repeated expensive queries, redundant API calls, recomputation). Applying it blindly wastes effort.

### Next prompt should include
- **App type** (web frontend, Node backend, React Native, etc.)
- **When slowness happens** (on load, during scrolling, specific action, under load, intermittent?)
- **How slow** (rough sense: 100ms lag, 2-second hang, etc.)
- **Relevant flow** (e.g., "user clicks a button → app fetches data → displays list")

With those details, I can give you the exact profiling steps for your stack and show you exactly where to add instrumentation.