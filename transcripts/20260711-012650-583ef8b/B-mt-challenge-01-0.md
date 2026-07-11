**Operating from: Upper-Left (Plan + Verify)**

This is a big shift. Let me recalibrate.

### What I understand now
You have Postgres as your only available store, caching may not be the right problem to solve, and you need to figure out what actually will improve API performance.

<assumptions>
  <project>Postgres is your only available persistent store; no Redis, Memcached, or external cache layer possible</project>
  <task>Improve API performance, but the root cause is unclear — it might not be cache-miss latency</task>
  <operator>You want to step back and diagnose before building</operator>
</assumptions>

### What I need to understand before proceeding
- **What's the actual symptom?** Slow API responses? High database load? High CPU/memory? Intermittent timeouts?
- **Have you measured?** Response time percentiles (p50, p95, p99)? Query execution times? How many concurrent users?
- **Where's the time going?** Is it network round-trips, query execution, data processing, or something else?
- **What queries are slow?** Do you have slow query logs enabled? Which endpoints are the bottleneck?
- **Current load profile.** QPS, data size, query complexity?

### Why this matters
Caching is a *symptom fix*, not a root cause fix. Before Redis (or before Postgres-native caching), you need to know:
- Is the database query actually slow, or is it the network overhead?
- Are you missing indexes?
- Are you fetching too much data (N+1 queries)?
- Is your schema normalized when it should be denormalized?

Each points to a different fix — and some are cheaper and simpler than adding a cache layer.

### Recommended path
Skip the Redis config. Instead:

1. **Enable slow query logging** on Postgres (if not already)
2. **Capture one day of real traffic** and identify your top 5 slowest queries by total time
3. **Share those queries + their execution plans** (EXPLAIN ANALYZE output)
4. **Tell me the symptom** you're trying to fix

Once I see that, I can tell you whether you need caching at all, or whether indexes, query restructuring, or schema changes are the real fix.

### Next prompt
Instead of asking for Redis config, say something like:

> "Our product API has been slow the last week. The `/search` endpoint takes 2-3 seconds at p95. Here are the top 3 queries by total time from our slow query log: [paste queries + EXPLAIN ANALYZE]. Our infrastructure is [deployment style]. Our API language is [language]."

That gives me enough to actually diagnose.