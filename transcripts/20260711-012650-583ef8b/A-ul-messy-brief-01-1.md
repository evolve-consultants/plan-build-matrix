# Finding Your Performance Bottleneck

Before jumping to caching, identify what's actually slow:

## 1. **Measure first**
- Use browser DevTools (Network, Performance tabs) or your app's profiler
- Log response times for different operations
- Check: API calls, database queries, rendering, computations
- Ask: Is it slow on first load? After interactions? For specific users?

## 2. **Look for the obvious culprits**
- **Repeated API calls** - same data fetched multiple times?
- **Large queries** - fetching more data than needed?
- **Synchronous operations** - blocking work on the main thread?
- **Unoptimized images/assets** - large file sizes?
- **N+1 queries** - looping and querying in a loop?

## 3. **Consider if caching helps**
Caching is best for:
- Data that doesn't change frequently
- Expensive operations (API calls, database queries, calculations)
- Data accessed repeatedly

**Not ideal for:**
- Highly dynamic data
- User-specific sensitive data (without careful TTLs)
- When you don't know the bottleneck

## Quick start
```javascript
// Simple example - cache API results
const cache = new Map();

async function fetchData(url) {
  if (cache.has(url)) return cache.get(url);
  
  const data = await fetch(url).then(r => r.json());
  cache.set(url, data);
  return data;
}
```

**What specifically feels slow?** That'll help narrow down what to cache.