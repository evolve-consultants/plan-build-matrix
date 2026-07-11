**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You want a learning roadmap for offline support — the core concepts arranged so you can build understanding from ground up, rather than jumping to implementation details.

<assumptions>
  <project>This is a web app (likely client-side JavaScript). I'm assuming you don't have offline support yet.</project>
  <task>You want to understand the *why* and *what* before the *how* — concepts, not code tutorials.</task>
  <operator>You're technically capable but may be new to offline patterns specifically.</operator>
</assumptions>

### What I'm unsure of
- Whether you care more about **offline-first** (sync-heavy, works great offline) vs. **offline-capable** (works online, degrades gracefully offline)
- Whether your app is **real-time collaborative** (multiple users, conflict resolution matters) or **single-user/simple sync**
- Time constraints — are you learning for immediate implementation or building knowledge first?

### Here's the breakdown (assuming offline-capable, single-user focus):

1. **State synchronization problem** — Why offline breaks most apps
   - Online apps assume the server is the source of truth
   - Offline, you're working with stale data and need to reconcile changes later
   - The core problem: handling conflicts when local changes meet server truth

2. **Storage layer abstraction** — How to decouple data from the network
   - Your app currently reads/writes directly to the server
   - You need a local cache (IndexedDB, SQLite, etc.) that *also* serves as your data layer
   - Both online and offline code read from the same place; sync is a separate process

3. **Sync mechanics** — How to bring offline changes back online
   - Queuing: what changes happened while offline, in what order
   - Reconciliation: comparing local state with server state and resolving conflicts
   - Idempotency: ensuring replay of failed requests doesn't corrupt data

4. **Network detection and retry strategy** — How to handle the fuzzy boundary between online/offline
   - Connection state isn't binary (you might have a connection but no real internet)
   - Retry backoff: exponential delays prevent hammering a recovering server
   - Optimistic updates: show results immediately, sync in background

5. **Conflict resolution and eventual consistency** — How to handle divergent versions
   - When local and server versions disagree, what wins?
   - Last-write-wins, operational transforms, or domain-specific logic
   - "Eventual consistency" means accepting that sync takes time; users may see different data briefly

### Recommended path
Start with **#1 (sync problem)** and **#2 (storage layer)** because they're the mental model shift—once you understand those, the rest is implementation. Skip #5 initially if your app is simple (no collaborative editing, users don't care about conflicts).

### Next prompt should include
- Confirmation of offline-capable vs. offline-first
- Whether your app has **real-time collaboration** or is **single-user**
- Which of these 5 you want me to expand into a deeper concept doc