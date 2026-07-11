# Deconstructing Offline Support for Web Apps

## 1. **Service Workers (The Foundation)**
Before anything else, you need to understand service workers—the background scripts that act as a programmable proxy between your app and the network. Key concepts:
- Lifecycle (install, activate, fetch events)
- Scope and registration
- How they intercept network requests
- The fact that they run separately from your main thread

Without grasping this, nothing else will make sense—it's the mechanism that makes offline functionality possible at all.

## 2. **Caching Strategies**
Once you understand service workers can intercept requests, you need to know *what to do* with those requests:
- **Cache-first**: Check cache, fall back to network
- **Network-first**: Try network, fall back to cache
- **Stale-while-revalidate**: Serve cache, update in background
- **Cache-only/Network-only**: For specific edge cases

Different resources (app shell vs. API data vs. images) often need different strategies.

## 3. **The Cache API & Storage Management**
Now you need to know *where* cached data actually lives:
- Using the Cache Storage API to store request/response pairs
- Storage quotas and eviction policies (browsers can clear your cache under pressure)
- Versioning caches so updates don't break things
- Cleaning up old caches during the activate event

## 4. **Data Persistence Beyond Static Assets (IndexedDB)**
Caching files is one thing, but offline apps usually need to store and query *dynamic data*:
- IndexedDB for structured, queryable client-side storage
- When to use IndexedDB vs. Cache API
- Handling larger datasets that won't fit in simple caches

This is where things shift from "offline viewing" to "offline functionality."

## 5. **Sync & Conflict Resolution (The Advanced Layer)**
The hardest part: reconciling offline actions with the server once connectivity returns:
- Background Sync API for queuing actions taken offline
- Conflict resolution strategies (last-write-wins, merge strategies, operational transforms)
- Optimistic UI updates and rollback handling
- Detecting online/offline state transitions gracefully

---

**Suggested learning path**: Master 1–2 first with a simple static app (like caching an app shell). Then move to 3–4 by adding a data-driven feature that works offline. Only tackle 5 once you have a real use case requiring bidirectional sync—it's genuinely complex and easy to over-engineer prematurely.