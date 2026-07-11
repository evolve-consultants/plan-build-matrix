# 5 Key Ideas for Offline Web App Support

## 1. **The Service Worker** (Foundational)
A JavaScript worker script that runs separately from your main app, acting as a proxy between your web app and the network. It intercepts requests and can serve cached content when offline. Think of it as a middleman that decides what gets cached and when.

## 2. **Cache Strategy Patterns** (Building Block)
Different approaches to *when* and *how* you store data:
- **Cache-first**: Use stored data if available, fall back to network
- **Network-first**: Try the internet first, use cache if offline
- **Stale-while-revalidate**: Serve cache immediately while refreshing in background

Choose based on your content's freshness requirements.

## 3. **Storage Mechanisms** (Building Block)
Where to actually store your offline data:
- **Cache API**: For HTTP requests/responses (service worker native)
- **IndexedDB**: For large structured data (like a local database)
- **LocalStorage**: For small key-value pairs (but blocks the main thread)

Each has different size limits and performance characteristics.

## 4. **State Synchronization** (Intermediate)
Managing the gap between offline and online states:
- Detecting connection changes
- Queueing user actions while offline
- Reconciling conflicts when syncing back (whose data wins?)
- Handling partial syncs and retry logic

## 5. **Offline-First Architecture** (Advanced)
Redesigning your app to treat offline as the default, not an edge case:
- Optimistic UI updates (assume actions succeed)
- Conflict resolution strategies for concurrent edits
- Progressive sync and background sync APIs
- Rethinking your backend API design around eventual consistency

---

**Start with #1-2** to get something working, then tackle #3 based on what you're storing.