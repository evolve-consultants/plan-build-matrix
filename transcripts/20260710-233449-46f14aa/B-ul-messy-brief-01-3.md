**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You're experiencing intermittent slowness in your app and suspect caching could be part of the solution, but you need a systematic way to identify the actual bottleneck before implementing anything.

<assumptions>
  <project>You have a running application (web, mobile, backend — unclear which). You have some ability to measure or observe performance.</project>
  <task>You want to locate the source of slowness so you can decide whether caching is the right fix and where to apply it.</task>
  <operator>You're looking for a diagnostic process, not a caching implementation yet. You probably haven't profiled or instrumented the app yet.</operator>
</assumptions>

### What I'm unsure of
- **What type of app** (web frontend, backend API, mobile, monolith, microservices)?
- **What "slow sometimes" means** — is it consistent latency, occasional spikes, or degradation over time?
- **What users experience** — slow page load, slow API responses, slow database queries, UI jank?
- **What you've already measured** — do you have any logs, metrics, or timing data, or is this based on observation?
- **Your stack** — what language, framework, database, infrastructure?

### Options

| | Approach | Upside | Downside | Best when |
|---|---|---|---|---|
| **A: Instrumentation first** | Add timing/tracing to identify where time is spent (database queries, API calls, computation, rendering) | Pinpoints the real bottleneck; avoids solving the wrong problem | Takes a little setup work; requires some code changes | You have no baseline data yet and need certainty before investing in caching |
| **B: Profiling + metrics** | Use existing APM/profiling tools (or add simple ones) to capture CPU, memory, and call stacks during slowness | Catches unexpected culprits (memory leaks, GC pauses, N+1 queries) | Requires tool selection; may generate noise if slowness is intermittent | You suspect systemic issues or want a full picture of resource use |
| **C: User feedback + logging** | Ask users when/where it's slow; correlate with timestamps in logs to find patterns | Fast, low overhead, user-centric | May miss technical root causes; anecdotal | Slowness is clearly user-facing and you want to prioritize what matters |
| **D: Cache speculatively** | Implement caching in likely places (database query results, API responses, computed data) and measure before/after | Fast to start; caching often helps anyway | High risk of solving the wrong problem; may add complexity without benefit | You've already identified the slow operations and are confident caching helps |

### Recommendation
**Start with Option A (Instrumentation)**, then move to B if needed.

Here's why: caching is a common fix but it only works if you're actually slow on I/O or computation—not on network, not on rendering, not on something else. Five minutes of strategic logging now saves you days of chasing the wrong fix. Once you know what's slow, the caching strategy becomes obvious.

### Next prompt should include
- **What type of app** (frontend, backend, etc.) and **what stack** you're using
- **How you experience the slowness** (what the user sees)
- **Whether you have any observability in place** (logs, metrics, APM tools, or starting from zero)
- **How reproducible it is** (consistent, random, under load, at certain times of day)

Once I know these, I can give you the exact instrumentation steps for your specific stack.