**Operating from: Upper-Left (Plan + Verify)**

This is a critical signal. Stop before building. Let me reframe:

<assumptions>
  <project>
    - You have Postgres available
    - Redis is ruled out by infra constraint
    - You don't yet have a caching layer deployed
  </project>
  <task>
    - You want to improve API performance
    - You initially thought caching was the answer, but now you're unsure
  </task>
  <operator>
    - You own the decision on whether caching is actually needed
    - You're willing to reconsider the problem, not just the solution
  </operator>
</assumptions>

### What I need to know before proceeding

1. **What's the actual problem?** 
   - Slow response times? Which endpoints? (p50, p99 latencies?)
   - High database load? (CPU, connection count, query time?)
   - Throughput bottleneck? (hitting request limit?)
   - User complaints about specific features?

2. **Who decided caching was the fix?**
   - Did you profile and find that N% of requests are cache-hits-in-waiting?
   - Or was it "APIs need caching" conventional wisdom?

3. **What does the slow path look like?**
   - Is it a complex query, N+1 queries, or network round-trip?
   - Is the same data requested repeatedly, or is every request unique?

### Why this matters

- **If you have N+1 queries**, caching helps but fixing the query is better
- **If you have one slow join**, an index or denormalized column might be the move
- **If you have repeated requests for the same data**, Postgres query result caching (or application-level in-memory cache with Postgres as source-of-truth) could work
- **If every request is unique**, caching won't help and you need to optimize the query itself

### The path forward

**Before I recommend a solution**, tell me:

1. **How did you identify that performance was a problem?** (metrics, user reports, load testing?)
2. **Show me one slow query or endpoint.** (SQL, response time, what it does)
3. **Is the data in that query repeated across requests, or is it unique per request?**

Once I see the actual bottleneck, I can tell you whether you need caching at all, and if you do, how to build it with just Postgres (query result tables, materialized views, or in-memory application cache with Postgres as source).

What's the actual performance issue you're trying to solve?