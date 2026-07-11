**Operating from: Upper-Left (Plan + Verify) — major assumption shift**

This is a critical pivot. Let me recalibrate before giving you any config.

<assumptions>
  <project>You have Postgres. Redis is off the table. Caching was your working hypothesis, not confirmed as the actual bottleneck.</project>
  <task>You're trying to solve a performance problem with your product API — but we haven't identified what the problem actually is yet.</task>
  <operator>You have autonomy to reconsider the approach, not locked into "add caching."</operator>
</assumptions>

### What I need to understand first

Before recommending anything, I need to know:

1. **What's the actual symptom?**
   - Is the API slow? (response time, p99 latency?)
   - Is it hitting resource limits? (CPU, memory, connections?)
   - Is throughput dropping under load?
   - Are specific endpoints slow or all of them?

2. **What have you measured?**
   - Do you have logs/metrics showing where time is spent? (query time, app processing, network?)
   - Is the database the bottleneck or something else?
   - Have you profiled the slow queries?

3. **What does the current query pattern look like?**
   - Are you doing N+1 queries?
   - Running expensive aggregations?
   - Missing indexes?
   - Fetching huge result sets?

### Why this matters

If caching wasn't actually your problem, adding it (even via Postgres) wastes effort. The real fixes might be:
- **Query optimization** (indexes, query rewrite, join logic)
- **Connection pooling** (if you're connection-starved)
- **Pagination/filtering** (if you're fetching too much data)
- **Denormalization or materialized views** (if reads dominate writes)
- **Read replicas** (if you have read-heavy workloads)

Each has a completely different config and setup.

### Next prompt should include

- What symptom prompted the "we need caching" decision?
- What metrics are you seeing that suggest a problem?
- Can you share an example of a slow query or endpoint (sanitized)?
- How much data are we talking about (product count, typical query size)?

Once I see the actual problem, I can recommend whether Postgres-native solutions (like materialized views, better indexes, connection pooling) are the right fix — or if something else entirely is.