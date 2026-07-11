# Adding Offline Support: 5 Key Ideas (Foundation → Advanced)

## 1. **What "offline" actually means**
Understand that offline support isn't binary. Users experience a spectrum: full connectivity, spotty networks, deliberate offline mode, or complete disconnection. You're building for graceful degradation, not a switch.

## 2. **Client-side storage fundamentals**
Before syncing or caching strategies, you need a reliable place to store data locally: localStorage (simple, limited), IndexedDB (robust, large capacity), or SQLite variants. This is where your app "remembers" things without the server.

## 3. **The cache-first vs. network-first tradeoff**
Different data types need different strategies. Should you serve cached content immediately then update it? Or always try the network first? This decision shapes your entire architecture and user experience.

## 4. **Sync conflict resolution**
When a user edits something offline and the server has a different version, what wins? You need a strategy: last-write-wins, merge logic, user prompts, or operational transforms. This is where offline gets philosophically complex.

## 5. **Service Workers as the enabling layer**
Once you understand the above, Service Workers become the tool that glues it together—they intercept network requests, manage caches, handle background sync, and run code even when your tab is closed.

---

**Start with #1-2, prototype #3, then tackle #4 only when you hit real conflicts.** Most projects don't need #5 immediately.