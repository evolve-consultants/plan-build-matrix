# Finding and Fixing Slowness

Start by **identifying the actual bottleneck** rather than guessing:

## Diagnosis First

1. **Use profiling tools**
   - Browser DevTools (Network, Performance tabs)
   - Application Performance Monitoring (APM) tools
   - Backend profilers (depends on your stack)

2. **Ask specific questions**
   - Is it slow on first load or subsequent visits?
   - Does it happen during specific actions (searches, filters)?
   - Is it a backend response time issue or frontend rendering?
   - Does it affect all users or specific ones?

3. **Check obvious things**
   - Network requests (too many? large payloads?)
   - Database queries (N+1 problems?)
   - Large computations or loops

## Then Consider Caching

Caching helps, but only for the *right* problems:

- **Slow API responses** → cache data client-side or with a cache layer
- **Expensive computations** → memoize or cache results
- **Repeated database queries** → query optimization or caching layer (Redis)
- **Static assets** → HTTP caching headers

Caching the wrong thing wastes effort and can cause stale data issues.

## Quick wins to try first
- Lazy load / code split
- Optimize images
- Reduce bundle size
- Database indexes
- CDN for static content

What kind of slowness are you seeing? (loading time, responsiveness during use, etc.) That would help narrow it down.