# Finding Your Bottleneck First

Before implementing caching, diagnose where time is actually being spent:

## Quick diagnosis steps

**1. Use profiling tools**
- Browser DevTools (Network, Performance tabs)
- Backend profilers (APM tools like New Relic, DataDog, or open-source alternatives)
- Database query logs/EXPLAIN plans

**2. Identify the slowest operations**
- Is it API requests? (network tab)
- Database queries? (slow query logs)
- Rendering? (Performance tab)
- Computation? (profiler)

**3. Measure before/after**
- Establish baseline metrics
- Only then try optimizations

## Common caching wins (in order of impact)

| Layer | Best for | Example |
|-------|----------|---------|
| **Database** | Expensive queries | Results, aggregations |
| **API/App** | Repeated requests | User data, configs |
| **Browser** | Static assets | CSS, JS, images |

## Red flags to check first

- Unoptimized database queries (N+1 problems, missing indexes)
- Excessive API calls for the same data
- Rendering the entire DOM when only parts change
- No HTTP caching headers set

**What type of slowness are you seeing?** (e.g., specific features, after certain actions, consistently?) That'll help point to the right solution—caching might not even be needed.