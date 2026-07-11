**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You're experiencing performance issues in your app, suspect caching could be part of the solution, but don't have clear visibility into *where* the slowness actually is — so you're looking for a diagnostic approach before jumping to implementation.

<assumptions>
  <project>You have a running app (web, mobile, or backend — unclear which); some baseline understanding of your tech stack; probably not currently instrumented with detailed performance metrics</project>
  <task>You want to identify the actual bottleneck(s) before investing time in caching, which may or may not be the right lever</task>
  <operator>You're looking for a structured method, not just "add caching everywhere"; you own the verification (you'll run the diagnostics yourself)</operator>
</assumptions>

### What I'm unsure of
- **What kind of app** (web frontend, backend API, mobile app, full-stack?)
- **What "slow sometimes" means** — is it consistently slow under load, slow on cold start, slow after running for a while, slow for specific operations?
- **What your current instrumentation looks like** — do you have logs, APM tools, browser dev tools, or are you going from user reports?

### The diagnostic path (recommended)
Rather than guessing at caching, find the actual bottleneck first. This almost always saves time.

1. **Identify the slow operation**
   - What specific action feels slow to users? (page load, API call, search, data processing?)
   - Can you reproduce it?

2. **Measure it**
   - Use your browser's Network tab (frontend), backend logs/APM (APIs), or Lighthouse/WebPageTest (full pages)
   - Get baseline numbers: How long does it actually take?

3. **Identify the culprit**
   - Is it network latency? (slow API call)
   - Is it computation? (heavy processing on the server or client)
   - Is it data fetching? (repeated queries, large payloads)
   - Is it rendering? (too much DOM work)

4. **Then consider caching**
   - Once you know *what's slow*, you can decide if caching helps
   - Different bottlenecks need different solutions (some don't benefit from caching at all)

### Next prompt should include
- **What type of app** you're building
- **Which operation feels slow** (or a specific user-facing symptom)
- **What your tech stack is** (frontend framework, backend language, database, etc.)
- **Whether you already have any performance data** — even rough (e.g., "API calls take 5 seconds")

Once I know these, I can walk you through the exact diagnostic steps for your environment, or jump straight to implementation if you've already identified the bottleneck.