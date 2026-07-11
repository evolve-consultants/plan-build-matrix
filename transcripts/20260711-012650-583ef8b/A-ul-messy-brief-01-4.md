# Start by identifying the actual bottleneck

Before adding caching, measure where time is actually being spent:

## Quick diagnosis steps

1. **Profile your app**
   - Use built-in tools (DevTools, Activity Monitor, etc.)
   - Look for functions/operations taking the most time
   - Check network requests, database queries, heavy computations

2. **Watch for common slow patterns**
   - Database queries running in loops
   - Repeated API calls for the same data
   - Large computations on every render/request
   - Synchronous operations blocking execution

3. **Check user-facing slowness**
   - Is it the initial load? → consider data fetching/bundling
   - Is it interactions? → likely computation or re-renders
   - Is it specific features? → narrow focus there

## Then consider caching layers (in order)

| Problem | Solution |
|---------|----------|
| Repeated identical API calls | HTTP cache headers, client cache |
| Database queries | Query result caching (Redis, in-memory) |
| Expensive computations | Memoization, precomputation |
| Re-renders with same props | React.memo, useMemo, Redux |

## Example: Don't cache blindly

```javascript
// ❌ Caching without knowing the problem
const cachedData = useMemo(() => expensiveFunction(), []);

// ✅ Cache only after profiling shows it's slow
// Profile first → confirm expensiveFunction is the bottleneck → then cache
```

**What does your app do?** (web, mobile, what kind of data?) I can give more specific advice if you share that.