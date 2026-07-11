**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You want a learning path for offline support — broken into 5 conceptual blocks, ordered so each one builds on the last, starting from fundamentals.

<assumptions>
  <project>You have a web app (React/Vue/vanilla—unclear which); unsure whether you've already implemented any caching, service workers, or data sync</project>
  <task>You want to understand offline support deeply enough to make architectural decisions, not just follow a tutorial</task>
  <operator>You're comfortable with web fundamentals (HTTP, browsers, client-side JS) but may be new to offline-specific patterns</operator>
</assumptions>

### What I'm unsure of
- What kind of app: simple document editor, real-time multiplayer, data-heavy CRUD, etc.? (affects which patterns matter most)
- Existing tech stack and what's already in place
- How much offline time you need to handle (minutes? days? indefinite?)
- Whether you need conflict resolution (two devices editing the same data offline, then syncing)

---

## The 5-step foundation

1. **The offline boundary: What actually needs to work without the network?**
   - Foundational because everything else depends on drawing this line correctly
   - Understand: read-only vs. write, which features, which data, acceptable staleness
   - Why first: if you don't know this, you'll over-engineer or under-engineer

2. **Storage primitives: Where does offline data actually live?**
   - Builds on #1 (now you know *what* to store)
   - LocalStorage vs. IndexedDB vs. SQLite (WASM) — tradeoffs in size, queryability, durability
   - Why second: you need a mental model of storage before you can architect caching or sync

3. **The service worker: How does a web app intercept and respond to requests offline?**
   - Builds on #2 (you know what you're storing and where)
   - Service workers are the mechanism that makes offline work; they sit between your app and the network
   - Why third: this is the engine that powers most offline patterns; you can't reason about the rest without it

4. **Caching strategies: When and how do you populate offline storage?**
   - Builds on #1–3 (you know what to cache, where to put it, and how to serve it)
   - Cache-first vs. network-first vs. stale-while-revalidate, preemptive caching, cache invalidation
   - Why fourth: strategy decisions flow from understanding storage and service workers

5. **Sync and conflict resolution: How do changes made offline merge back when the network returns?**
   - Builds on all of #1–4 (assumes you understand boundaries, storage, serving, and caching)
   - Last-write-wins vs. operational transform vs. CRDTs, detecting conflicts, merging strategies
   - Why last: this is the hardest piece; you only get here once the basics work

---

### Recommendation
Start with #1–2 together (they're deeply linked). Get clarity on your offline boundary and storage choice before reading about service workers.

### Next prompt should include
- What kind of app and what features absolutely need to work offline?
- Rough size of data that needs offline access?
- Whether you've sketched out which data needs to sync back vs. stay local
- Whether you want me to expand one of these 5 into a detailed primer, or move straight to implementation planning