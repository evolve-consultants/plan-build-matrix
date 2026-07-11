**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You're experiencing intermittent slowness in your app and suspect caching could help, but you need to identify where the bottleneck actually is before you implement a fix.

<assumptions>
  <project>You have a web or mobile app of some kind; I don't know the tech stack, architecture, or scale</project>
  <task>You want to diagnose the slow spots and determine whether caching is actually the right lever</task>
  <operator>You're willing to do some measurement work but want a structured approach that doesn't require deep profiling knowledge</operator>
</assumptions>

### What I'm unsure of
- **Tech stack**: Is this a web app (frontend/backend split?), mobile app, monolith? Framework? Database?
- **When slowness happens**: Is it consistent or random? On first load, after heavy use, under load spikes?
- **What feels slow**: Page load time, API responses, database queries, rendering, something else?
- **Current setup**: Do you have any observability in place (logging, monitoring, performance metrics)?
- **Scope**: Is this production slowness affecting users, or development/testing slowness?

### Options

| | What to do | Cost | Best when |
|---|---|---|---|
| **A: Measure first** | Profile the app end-to-end (network, compute, database) before touching anything. Identify the actual bottleneck. Then decide if caching helps. | Time upfront, but eliminates guesswork | You want high confidence the fix will matter. You can tolerate slow diagnosis. |
| **B: Common-sense caching** | Cache at the obvious layers (API responses, database queries, static assets) based on domain knowledge. Monitor if it helps. | Quick to implement; risk of over-caching. | You're under time pressure and confident you know where the problem is. |
| **C: Hybrid — quick check then measure** | Do a fast 15-minute smell test (load times, network tab, slow query log), identify the likely culprit, then measure that specifically. | Low overhead. Fast feedback. | You want to move quickly but stay grounded in data. |

### Recommendation
**Option C** — do a quick diagnostic pass first so we're not flying blind, then measure the specific layer you suspect is slow. This keeps you from either over-engineering a solution or chasing a phantom problem.

### Next prompt should include
- Your tech stack and deployment environment
- When the slowness happens (consistently or sporadically?)
- What user action triggers it
- Whether you have any monitoring or logging in place already

Once I know these, I can give you a specific measurement plan that takes 30 minutes and tells you exactly where to optimize.