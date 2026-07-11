# Finding Your Performance Bottleneck First

Before caching, identify what's actually slow:

## Quick diagnostics

**Browser DevTools (easiest start)**
- Open DevTools → Network tab
- Look for slow requests or large payloads
- Check Performance tab for JavaScript bottlenecks
- See what takes the longest

**Backend logging**
- Add timestamps to key operations
- Time database queries, API calls, external services
- Look for patterns (specific endpoints? certain times?)

**User feedback**
- Where do users say it's slow?
- Is it initial load, interactions, specific features?

## Common culprits (in rough priority)

1. **Database queries** — N+1 queries, missing indexes, fetching too much data
2. **External API calls** — Slow third-party services
3. **Large initial payloads** — Too much data sent at once
4. **Unoptimized code** — Expensive loops, unnecessary calculations
5. **Missing indexes** — Database scans instead of lookups

## What to do now

1. **Measure first** — Use your browser/backend tools to find the actual slow part
2. **Share specifics** — "API takes 5 seconds" or "initial load is 8MB" helps a lot
3. **Try cheap wins first** — Database indexes, query optimization, code fixes often beat caching
4. **Then cache strategically** — Once you know what's slow, cache that specific thing

**What kind of slowness are you seeing?** (page load, interactions, specific features?) That'll help narrow down where to look.