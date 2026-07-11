**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You're experiencing performance issues in your app, suspect caching could help, but don't have a clear picture of where the bottleneck actually is. You want guidance on how to find it and whether caching is the right fix.

<assumptions>
  <project>You have a web or mobile app with a backend; I don't know the tech stack, data volumes, or architecture</project>
  <task>You want to identify the root cause of slowness and determine if caching solves it (rather than, say, query optimization or infrastructure scaling)</task>
  <operator>You have access to logs, monitoring tools, or can instrument the app; you're open to systematic investigation rather than guessing</operator>
</assumptions>

### What I'm unsure of
- **Tech stack**: frontend, backend, database, hosting (this changes tools and strategies)
- **When slowness occurs**: all the time, under load, intermittently, on specific features?
- **What "slow" means**: 5 seconds vs 500ms feels very different and requires different fixes
- **Current observability**: do you have logging, metrics, APM tools, or are you flying blind?
- **Caching assumption**: why do you think caching specifically? User reports, intuition, or prior experience?

### Options

| | Approach | Upside | Downside | Best when |
|---|---|---|---|---|
| **A: Instrument first, diagnose later** | Add logging/timing to identify slowest code paths without assumptions | Find the *real* bottleneck; avoid wasted effort on wrong fixes | Takes time upfront; requires code changes | You have no current metrics and can't afford to ship a cache that doesn't help |
| **B: Profile under load** | Use APM tools (New Relic, Datadog, etc.) or built-in profilers to see where time is spent | Fast visibility; captures real production behavior | Costs money; requires tool setup; may need deploy | You're running in production and can tolerate a tool installation |
| **C: Implement caching speculatively** | Add caching to likely hot paths (database queries, API calls, expensive computations) and measure impact | Fast to try; might work; teaches you about your data flow | Ships blind; could hide the real problem; wastes effort if bottleneck is elsewhere | You've already narrowed it down to specific features and are confident about what to cache |
| **D: Hybrid — quick manual profiling** | Add `console.time()` / logging to suspected slow sections; run real user workflows; see what takes time | Requires no tools; quick to implement; gives directional data | Less precise than APM; manual; limited to what you instrument | You're on a tight timeline and just need directional answers |

### Recommendation
**Start with Option D** (manual profiling of suspected paths) because:
1. It's the fastest path to *any* data
2. It'll tell you if caching is even relevant (if the slowness is network latency vs. computation vs. rendering, caching has different value)
3. Once you find the bottleneck, you'll know exactly what to cache — no guessing
4. If results are unclear, *then* move to B (APM) for production-level visibility

### Next prompt should include
- Your tech stack (language, framework, database, frontend, hosting)
- An example: describe a slow user workflow end-to-end (what do they click, what do they see, where does it pause?)
- Whether you have any current logging or monitoring tools
- Once you've done quick profiling, share the timing results — that'll let me recommend specific caching strategies