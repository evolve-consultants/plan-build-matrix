# Diagnosing Performance Issues Before Adding Caching

Start by **measuring first**—caching the wrong thing wastes effort. Here's a practical approach:

## 1. Identify the actual bottleneck
- **Profile your app**: Use browser DevTools (Network, Performance tabs) or APM tools
- **Check the timeline**: Is it slow on initial load, after user actions, or specific features?
- **Look at server logs**: Are responses slow, or is the network the issue?

Common culprits:
- Slow database queries
- Large API responses
- Expensive computations
- Rendering/re-renders
- Network latency

## 2. Quick diagnostic questions
- Does it happen consistently or intermittently?
- Is it the *first* time accessing data, or *every* time?
- Are users seeing stale data as a problem?

## 3. Then consider caching strategically

**Cache if you see**:
- The same data requested repeatedly
- Expensive queries/computations
- Network calls that don't need real-time updates

**Example priorities**:
```
High-value targets:
- API responses (browser cache, Redis)
- Database query results
- Static assets (already handled by most servers)

Lower priority:
- Data that changes frequently
- User-specific data (unless properly isolated)
```

## 4. Measure improvement
After implementing caching, verify it actually helped using the same tools.

**What's your app's main function?** That'd help me suggest specific caching strategies that fit your situation.