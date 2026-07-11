**Shifting to: Upper-Left (Plan + Verify)**

This is a significant constraint change. Let me reset before we proceed.

<assumptions>
  <project>
    - Redis is now off the table; Postgres is your only option
    - You have a Postgres database already running for your product API
  </project>
  <task>
    - Originally: "set up caching layer"
    - Now: uncertain whether caching is the right fix at all
  </task>
  <operator>
    - You're reconsidering the entire approach, not just swapping Redis for Postgres
  </operator>
</assumptions>

### What I need to understand before moving forward

Right now I have a frame problem. "Caching layer" is a solution, but I don't know the **problem it's meant to solve**. Before we design anything, let's be explicit:

1. **What's the actual pain point?**
   - Is the API slow? (Latency? Throughput? Specific endpoints?)
   - Is Postgres hitting resource limits? (CPU? Memory? Disk I/O?)
   - Are you seeing timeout errors, or just subjective slowness?

2. **What made you choose "caching" as the fix?**
   - Did you profile and see the same queries running repeatedly?
   - Is there read-heavy traffic with data that changes infrequently?
   - Or was it a "caching is always good" assumption?

3. **What does your current data look like?**
   - How much data in Postgres? (GB? TB?)
   - How many requests/sec to the API?
   - What's the read/write ratio?
   - How often does cached data need to be fresh?

### Why this matters

If Postgres is your only option, the *shape* of the solution changes dramatically:
- **Query optimization** (indexes, query rewrite) often gives 10-100x speedup for free
- **Connection pooling** (PgBouncer) solves concurrency issues cheaply
- **Materialized views** can replace application caching for some workloads
- **Read replicas** distribute load without adding a new system
- **Actual caching in Postgres** (JSON columns, computed columns) is possible but has tradeoffs

But which of these matters depends on what's actually broken.

### Recommended next step

Before I design anything:

**Tell me:**
1. What specific behavior made you think "we need caching"? (Slow endpoint? Timeouts? High Postgres CPU?)
2. Have you profiled the API to see where time is actually being spent?
3. What does a typical request do? (Single query? Multiple queries? Complex joins?)

Once I understand the real problem, I can either:
- Confirm caching is the right fix and show you how to do it in Postgres
- Suggest a different fix that's faster/simpler
- Show you how to do both (optimize + cache strategically)

What's the actual symptom you're trying to fix?