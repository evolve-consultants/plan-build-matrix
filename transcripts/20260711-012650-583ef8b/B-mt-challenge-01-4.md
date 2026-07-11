**Operating from: Upper-Left (Plan + Verify)**

This is actually a critical pivot. Let me reframe before we do anything.

<assumptions>
  <project>You have a Postgres database. Redis is off the table — no option to add it.</project>
  <task>You identified a performance problem with your product API and proposed caching as the solution. Now that caching via Redis is blocked, you're reconsidering the root cause.</task>
  <operator>You want to solve the real problem, not force a tool that doesn't fit your constraints.</operator>
</assumptions>

### What I need to understand

Right now, I have three separate unknowns, and they all matter:

1. **What's the actual performance problem?**
   - Slow API endpoints (which ones, how slow?)
   - High database load?
   - Timeouts under load?
   - Something else?

2. **Why did you land on "caching" as the fix?**
   - Someone suggested it, or you ran load testing and saw specific bottlenecks?
   - Are you seeing repeated identical requests, or one-time slow queries?
   - Is the problem latency, throughput, or both?

3. **What's your current Postgres setup?**
   - Query performance: have you profiled slow queries (EXPLAIN ANALYZE)?
   - Hardware: is it resource-constrained (CPU, memory, disk)?
   - Schema: are there missing indexes, N+1 queries, or bloated tables?

### Why this matters

The "right" fix could be:
- **Query optimization** (indexes, query rewrite) — fastest, costs nothing, works in Postgres
- **Connection pooling** (PgBouncer) — if you're connection-limited
- **Caching *in* Postgres** (materialized views, partial indexes) — if you have hot data
- **App-level caching** (in-memory, SQLite sidecar, read replicas) — if you can't touch infra
- **API design change** (pagination, filtering, aggregation) — if the problem is payload size or scope
- **Actually not caching** — if the problem is write-heavy, cache invalidation would be a nightmare

### Recommended path

Give me:
- **One specific API endpoint or query that's slow** (include the SQL if you have it)
- **How slow** (latency, throughput, under what load?)
- **What data does it touch** (one table? joins? aggregations?)

Then I can help you diagnose whether caching would even help, or if there's a faster fix inside Postgres.

### Next prompt should include
"The problem is: [endpoint/query] takes [time] under [conditions]. Here's the query: [SQL]"

Or if you don't have SQL yet: "I don't know the exact bottleneck yet — how should I find it?"