# Finding and Fixing Your Speed Problem

Start with **diagnosis before solutions**—caching in the wrong place wastes effort.

## 1. Identify the actual bottleneck

**Measure first:**
- Use browser DevTools (Network tab) to see load times
- Check server logs for slow endpoints
- Profile your code (time DB queries, API calls, calculations)
- Monitor real user data if possible

**Ask yourself:**
- Is it slow on first load or after interactions?
- Does it happen consistently or intermittently?
- Is it frontend, backend, or both?

## 2. Common culprits (in order of likelihood)

| Issue | Signs | Quick fix |
|-------|-------|----------|
| Database queries | Slow API responses | Add indexes, optimize queries |
| Rendering large lists | Janky scrolling/interactions | Virtualization, pagination |
| Large assets | Slow initial load | Compress images, code splitting |
| Repeated identical requests | Network waterfall | Caching |
| Heavy computations | CPU spikes | Debounce, web workers |

## 3. When caching actually helps

Caching is the right answer for:
- ✅ Expensive operations you do repeatedly
- ✅ Data that doesn't change often
- ✅ API responses that can be stale briefly

Caching won't help:
- ❌ If you only do something once
- ❌ If data changes constantly
- ❌ If your bottleneck is rendering (not fetching)

## Next step

**What specifically feels slow?** (loading a page? UI interactions? data appearing?) That'll point to the real fix.