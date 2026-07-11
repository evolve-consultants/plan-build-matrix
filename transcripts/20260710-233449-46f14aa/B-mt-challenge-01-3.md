**Operating from: Upper-Left (Plan + Verify)**

Good — this is the moment to step back. You've just learned something that breaks the original assumption ("we've decided on Redis"). Let's recalibrate before rebuilding.

### What I understand now
Your infra can only provide Postgres. You're uncertain whether caching is the right solution at all.

<assumptions>
  <project>
    - You have Postgres available
    - Redis is off the table
    - Your product API reads from Postgres
  </project>
  <task>
    - You're experiencing some performance problem (slow API? high load? both?)
    - Caching was a guess at the fix, not a diagnosed requirement
  </task>
  <operator>
    - You want to solve the actual problem, not just implement a tool
  </operator>
</assumptions>

### What I need to understand first

Before recommending *any* solution, I need to know what problem you're actually solving:

1. **What's broken right now?** (slow response times? timeouts? high CPU/memory? database connection pool exhaustion?)
2. **How bad?** (P95 latency? error rate? user complaints? specific endpoint?)
3. **What does the product API do?** (simple product lookups by ID? filtering/search? aggregations?)
4. **What's your current query pattern?** (lots of repeated identical queries? or every request is different?)
5. **Have you profiled it?** (do you know where the time is spent — query execution, serialization, network?)

### Why I'm asking instead of jumping to a solution

Caching helps when:
- The same data is requested repeatedly (hit rate matters)
- Query execution is the bottleneck (not network, not serialization)
- Staleness is acceptable

Caching *won't* help if:
- Every request is unique (low hit rate)
- The real bottleneck is something else (connection pool, slow JSON serialization, network latency to infra)
- You need perfectly fresh data always

**You might actually need:** query optimization, connection pooling, database indexing, denormalization, pagination, or read replicas — all of which work with Postgres alone.

### Next prompt should include

Tell me:
- What specific performance problem are you seeing?
- One example query or API endpoint that's slow
- Whether you've checked query times in Postgres directly (via `EXPLAIN ANALYZE`)
- How much control you have over the API code (can you modify it freely?)

Once I see the actual problem, I can recommend the cheapest, fastest fix that works with what you have.