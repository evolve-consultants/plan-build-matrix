**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You've noticed performance dips in your app, suspect caching could help, but don't have a clear picture of what's actually slow or where to start. You want a path to diagnose the problem and decide if caching is the right fix.

<assumptions>
  <project>I'm assuming this is a web or mobile app, but I don't know the tech stack, whether it's backend-heavy or frontend-heavy, or what kind of work it does (UI rendering, database queries, API calls, compute).</project>
  <task>I'm assuming you want to move from "it feels slow" to "here's the bottleneck" to "here's whether/where to cache" — not a full caching implementation yet.</task>
  <operator>I'm assuming you have access to the running app and some ability to measure or observe its behavior, but I don't know your debugging familiarity or tooling setup.</operator>
</assumptions>

### What I'm unsure of
- **Tech stack**: Is this frontend (React/Vue/etc.), backend (Node/Python/Go/etc.), mobile, or a full stack? Language matters for tooling.
- **Type of slowness**: Does it happen during initial load, on repeated actions, under heavy use, or randomly? Pattern matters.
- **Scale of data**: Are you loading kilobytes, megabytes, or gigabytes? Caching value depends on this.
- **Where you suspect it**: Is it the UI being sluggish, API responses slow, database queries, or you genuinely don't know?

### Options

| | Approach | Upside | Downside | Best when |
|---|---|---|---|---|
| **A: Measure first** | Use built-in profiling tools to find the actual bottleneck before making changes | Catches false assumptions; you won't waste time caching the wrong thing | Takes time upfront; requires some tooling familiarity | You want high confidence and don't mind the investigation |
| **B: Target obvious candidates** | Add caching to the most likely culprits (API responses, database queries, expensive computations) based on domain knowledge | Fast to implement; often helps even if not perfectly targeted | Risk of caching the wrong layer; might not solve the real problem | You're confident about the slowness source or have done this before |
| **C: Hybrid approach** | Do a quick measurement pass to narrow down (frontend vs. backend vs. network), then cache the most likely bottleneck | Balance between speed and accuracy | Still requires some investigation but less deep | You want practical movement without guessing blind |

### Recommendation
**Start with Option A (Measure first)**, but scope it narrowly:

1. **Identify the bottleneck type** (5–10 minutes):
   - Is it **frontend** (UI janky/slow to respond)? Use browser DevTools Performance tab.
   - Is it **backend** (API responses slow)? Add simple timing logs around requests.
   - Is it **network** (waiting for data)? Check Network tab in DevTools.

2. **Locate the specific culprit** (what you measure depends on type):
   - Frontend: which component re-renders too often?
   - Backend: which endpoint/query is slow?
   - Network: how much time is actually spent waiting vs. processing?

3. **Then decide**: Does this look like a caching problem, or something else (N+1 queries, inefficient rendering, unoptimized assets)?

This takes 20–30 minutes and saves you from caching the wrong thing. If you jump straight to caching without knowing the problem, you might add complexity without fixing the real issue.

### Next prompt should include
- **Your tech stack** (language, framework, frontend/backend split)
- **When you notice the slowness** (page load, repeated clicks, specific feature, random?)
- **How confident you are** about where it's slow (total guess vs. strong hunch?)

Once I know those, I can give you the exact tools to measure and the specific caching strategy if measurement confirms it's the right fix.