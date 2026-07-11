Here's a practical frame for this decision:

**Start with the actual problems:**
- What's driving the GraphQL push? (Over-fetching? Multiple endpoint calls? Developer experience?)
- What are the "waste of time" concerns? (Migration cost? Complexity? Performance uncertainty?)

Get specific. "GraphQL is better" vs "REST works fine" are both too vague.

**Consider your real constraints:**
- How much maintenance burden is your current API?
- Do you have the GraphQL expertise, or would you be learning on the job?
- What's your migration path? (Parallel running? Big bang? Gradual?)
- Does your infrastructure (caching, monitoring, auth) need rework?

**Honest tradeoffs:**
- GraphQL wins: flexible queries, fewer round-trips, better for mobile/varied clients, stronger types
- REST wins: simpler caching, easier debugging, better HTTP semantics, larger ecosystem

**What often works:**
1. **Pilot, don't migrate everything** — Build *one* new service in GraphQL. See if the benefits materialize for your use cases.
2. **Hybrid approach** — Keep REST for stable, heavily-cached endpoints; use GraphQL for complex/variable query patterns.
3. **Postpone if...** your REST API isn't actually causing problems, you're learning GraphQL simultaneously, or you lack buy-in.

The real answer probably isn't "switch everything" or "never touch it." What specific problems are showing up in production?