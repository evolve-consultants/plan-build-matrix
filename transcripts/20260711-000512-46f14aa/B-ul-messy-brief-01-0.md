**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
Your app has performance issues, you suspect caching could help, but you haven't yet identified the actual bottleneck. You want a path forward.

<assumptions>
  <project>Unknown: I don't know your stack (web/mobile/API), scale, or architecture — could be frontend rendering, backend processing, database queries, or network latency.</project>
  <task>You want to fix real slowness, not just add caching reflexively — caching is a hypothesis, not a confirmed diagnosis.</task>
  <operator>Unknown: I don't know if you have logging/monitoring/profiling tools already in place, or your comfort level with performance tooling.</operator>
</assumptions>

### What I'm unsure of
- What kind of app this is (web app, mobile, API service, desktop)
- What "slow" means concretely — page load time, specific button clicks, background jobs, only under load, only for certain users?
- Whether you have any existing logs, APM tools (e.g., New Relic, Datadog), or ability to profile
- Whether the slowness correlates with anything (time of day, data size, specific endpoints/pages)

### Options
| | Upside | Downside | Best when |
|---|---|---|---|
| **A: Answer diagnostic questions first** | Fastest path to a correct fix; avoids wasted effort | Requires a bit of upfront info-gathering from you | You want the most accurate, tailored next step |
| **B: Follow a general profiling framework yourself** | Reusable skill, works regardless of stack, no back-and-forth needed | Slower, more self-directed, requires some tooling setup | You want to learn to diagnose this on your own or don't want to share details yet |
| **C: Just try common caching strategies now** | Fast to attempt, no diagnosis needed | High risk of solving nothing if bottleneck isn't cache-related (e.g., could be N+1 queries, slow third-party API, unoptimized frontend bundle) | You already have a strong hunch backed by *some* evidence (e.g., you've seen slow DB query logs) |

### Recommendation
**Option A** — answer a few diagnostic questions so I can point you at the actual bottleneck. Caching only helps if the slowness is from repeated expensive reads (DB queries, API calls, computed results) — it does nothing for things like slow rendering, network latency, or inefficient algorithms. Guessing wrong wastes effort and can add complexity (cache invalidation bugs) without fixing anything.

### Next prompt should include
- What type of app/stack this is
- What specifically feels slow (which action, page, or flow)
- Whether it's consistent or intermittent, and under what conditions
- Any existing logs, timings, or monitoring data you can share (even rough numbers help)