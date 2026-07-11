**Stopping here — major assumption collapse.**

You've just surfaced two things that change everything:

1. **Infrastructure constraint**: Redis is off the table. You're Postgres-only.
2. **Problem uncertainty**: You're not sure caching is actually the solution.

This means we shouldn't be configuring anything yet. We need to step back and diagnose.

### What I need to understand before proceeding

**On the constraint:**
- Is Postgres truly the only in-memory/fast-access layer available? (No memcached, in-process caching, or other stores?)
- Can you use Postgres extensions or features as a cache layer, or do you need something external?

**On the actual problem:**
- What's the symptom you're trying to fix? (slow API responses, database CPU, N+1 queries, something else?)
- What does "product API" performance look like right now? (response times, request volume, which endpoints are slow?)
- Have you profiled to confirm the bottleneck? (DB query time? serialization? network?)
- What made you initially think caching was the answer?

### The real next step

Before we design a solution, we need to confirm the problem. Caching helps with certain patterns (repeated reads of expensive queries) but not others (first-time requests, write-heavy workloads, data freshness requirements).

**Recommended next prompt:**
- Describe the performance issue in concrete terms (e.g., "product listing endpoint takes 3s for 100k results")
- Share profiling data if you have it, or describe what you've observed
- Tell me what your infra actually supports (Postgres only? Any other services? In-process caching okay?)
- I'll help you diagnose whether caching fixes it, and if so, how to do it with Postgres

Does that work?