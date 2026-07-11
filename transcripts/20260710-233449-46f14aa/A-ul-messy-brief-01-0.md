# Finding and Fixing Performance Issues

Start with **measurement** before jumping to caching—it often isn't the bottleneck.

## 1. **Identify the actual problem**

Use profiling tools to see where time is spent:
- **Backend**: Use APM tools (New Relic, DataDog, Prometheus) or built-in profilers
- **Database**: Check slow query logs, look for N+1 queries
- **Frontend**: Browser DevTools (Network, Performance tabs), Lighthouse
- **API calls**: Monitor response times and payload sizes

**Ask yourself:**
- Is it consistently slow or intermittently?
- Which specific actions/pages are affected?
- Is it network, computation, or I/O bound?

## 2. **Common issues (not always caching)**

- **Unoptimized queries** (missing indexes, loading unnecessary data)
- **N+1 query problems** (fetching related data in loops)
- **Large payloads** (transfer time, parsing time)
- **Synchronous operations** that should be async
- **Inefficient algorithms** or loops

## 3. **When caching actually helps**

- Frequently accessed data that changes infrequently
- Expensive computations with stable inputs
- Database queries that don't need fresh data every request
- Static assets (already done by CDNs)

## 4. **Start here instead**

1. **Profile** to find the bottleneck
2. **Optimize** the root cause (better query, async, algorithm)
3. **Cache** what remains expensive

---

What type of slowness are you seeing (backend, frontend, database)? That'll help narrow it down.