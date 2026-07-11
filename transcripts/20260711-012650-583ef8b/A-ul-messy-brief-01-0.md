# Finding Your Bottleneck First

Before adding caching, identify what's actually slow:

## Quick diagnosis steps

1. **Check your logs/monitoring**
   - Which requests are slowest?
   - Is it database queries, API calls, or computation?
   - Use tools like: New Relic, DataDog, or your framework's built-in profiler

2. **Profile specific operations**
   ```python
   import time
   start = time.time()
   # your code
   print(f"Took {time.time() - start}s")
   ```

3. **Database query analysis**
   - Run `EXPLAIN` on slow queries
   - Check for missing indexes
   - Look for N+1 query problems

## Common culprits (in rough order)

- **Database queries** (most common)
- **Expensive computations**
- **External API calls**
- **File system operations**
- **Rarely: app code itself**

## Once you know the problem

- **Slow database queries** → Index, optimize query, or cache results
- **External API calls** → Cache responses
- **Expensive calculations** → Cache computed values
- **Repeated file reads** → Cache in memory

## Avoid premature caching

Caching that doesn't target the real bottleneck adds complexity without benefit. You might cache the wrong thing or miss the actual issue.

**What does your monitoring show about where time is spent?** That'll help determine if caching is actually the right solution.