# Finding and Fixing Your Caching Problem

Start with **measurement** rather than guessing—caching in the wrong place can actually hurt performance.

## Step 1: Identify the bottleneck

Use profiling tools to find what's actually slow:

- **Backend**: Check database query times, API response times, CPU usage
- **Frontend**: Use browser DevTools (Network, Performance tabs)
- **Network**: Look for slow API calls or large payloads
- **Database**: Enable slow query logs

**Look for patterns:**
- Does it slow down at specific times?
- Does it happen on first load vs. subsequent visits?
- Is it particular features or the whole app?

## Step 2: Consider what to cache

The "best" targets, in order:

1. **Database queries** - Usually the biggest wins (if queries are slow, not network latency)
2. **API responses** - Especially external APIs
3. **Expensive computations** - Complex calculations, image resizing
4. **Static assets** - Browser/CDN caching (often already done)

## Step 3: Choose the right caching layer

| Layer | Good for | Example |
|-------|----------|---------|
| Database query cache | Repeated same queries | Redis, Memcached |
| HTTP caching | API responses | Browser cache, CDN |
| Application memory | Computed results | In-memory hash map |
| CDN | Static/media files | CloudFlare, AWS CloudFront |

## Quick diagnostic questions

- Is the slowness **consistent or intermittent**? (Intermittent suggests resource contention)
- Does it improve on **refresh**? (Yes = good caching candidate)
- Is it **user-specific or shared data**? (Shared data = easier to cache)

What type of app is this and what operations feel slowest?