**Operating from: Upper-Left (Plan + Verify)**

This is a bigger shift than swapping the tech — the constraint change (no Redis) and your doubt about caching mean we should step back before proposing any solution.

<assumptions>
  <project>Unknown: what "product API" actually does, what's slow, and what's driving the need for a caching layer in the first place</project>
  <task>Previously assumed "cache API responses" was the fix; that's now explicitly in question — the real task may be "reduce load/latency" rather than "add caching"</task>
  <operator>You're now the one flagging uncertainty, which suggests this request came from somewhere upstream (a perf complaint, a cost concern, a scaling worry) rather than a settled technical decision</operator>
</assumptions>

### What I'm unsure of
- What symptom prompted this — slow endpoints? High DB load? Rate limiting? Cost?
- Whether the bottleneck is actually confirmed (query profiling, APM traces) or inferred
- What's actually slow: repeated identical reads, expensive aggregations, N+1 queries, or something else entirely (network, serialization, external API calls)
- Read/write ratio and data volatility — does the "hot" data change often, or is it mostly static reference data

### Options

| | Upside | Downside | Best when |
|---|---|---|---|
| **A: Diagnose first** — profile slow queries/endpoints before choosing any fix | Avoids solving the wrong problem; may reveal an index or query fix that needs no caching layer at all | Takes longer before you have something to ship | You don't yet have hard evidence of *why* it's slow |
| **B: Postgres-native caching** — materialized views, `UNLOGGED` tables, or `pg_cached`-style read replicas | No new infra, works within your constraint | Doesn't help if the real issue is query complexity or write contention | Diagnosis confirms it's read-heavy, repeatable queries and infra really can't add a service |
| **C: In-process/application-level cache** (e.g. in-memory LRU inside the API process) | Zero new infra, trivial to add | Doesn't scale across multiple API instances, cache incoherence on scale-out | Single-instance API, or diagnosis shows a narrow set of very hot, cheap-to-store values |

### Recommendation
**Option A.** Given you're now unsure caching is even the fix, the highest-value next step is confirming *where* the time/load is actually going — not picking a caching mechanism. If profiling points to specific slow queries, the fix might be indexing or query restructuring, not caching at all. If it points to repeated identical reads, Option B or C follows naturally.

### Next prompt should include
- What symptom triggered this (specific slow endpoints, DB CPU/IO metrics, error logs, cost report — whatever you have)
- Whether you have query-level visibility (Postgres `pg_stat_statements`, APM tool, slow query log) or need help setting that up first
- Roughly how many API instances run concurrently (affects whether in-process caching is viable at all)