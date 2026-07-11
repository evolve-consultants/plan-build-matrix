**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You want me to break down offline support into a learning sequence — starting with the most basic concepts you need to grasp before tackling advanced implementation, so you can build mental models in the right order.

<assumptions>
  <project>You have an existing web app (tech stack unknown). You're planning to add offline capability, not building from scratch.</project>
  <task>You want a conceptual foundation before diving into code/tools. You need to understand the "why" and "what" before the "how."</task>
  <operator>You're technically capable but may not have thought deeply about offline architecture before. You want the sequence that minimizes backtracking.</operator>
</assumptions>

### What I'm unsure of
- What type of web app (CRUD-heavy, real-time, read-mostly, etc.) — this affects which concepts matter most
- Whether you're targeting service workers / PWA specifically, or open to other approaches
- Your tolerance for data freshness complexity (eventual consistency vs. strong guarantees)

---

## Here's the deconstruction (Foundational → Advanced)

### 1. **State Synchronization Model**
*Why it matters first:* Everything else depends on how you think about data when the network is split. Do you sync before rendering? After? Both? What's the source of truth?

**The core idea:** Offline data lives locally; online data lives server-side. You must choose: is the server the primary source (fetch-then-cache) or is local storage primary (cache-then-sync)? This decision shapes every layer below it.

**Why it's foundational:** Without clarity here, later decisions feel arbitrary.

---

### 2. **Storage Layer (Local Data Persistence)**
*Why it matters second:* Now that you know your sync model, you need a place to store data locally. This is mechanical but critical.

**The core idea:** Browser storage exists on a spectrum: `localStorage` (simple, small), `IndexedDB` (large, queryable, async), `SQLite` (when using Electron/Tauri). Each trades simplicity for power.

**Why it's foundational:** You can't sync or use offline data without a place to keep it. But you don't need to choose the storage *technology* until you understand *what* you're storing and *why*.

---

### 3. **Conflict Resolution**
*Why it matters third:* The hard problem. When the user edits offline and the server also changed, what wins? How do you decide?

**The core idea:** You need a strategy: last-write-wins (simple, lossy), field-level merging (complex, preserves intent), manual UI resolution (safe, slow), operational transformation (powerful, rare in web apps).

**Why it comes here:** You can design storage and sync mechanics without this, but you'll discover the gap quickly. Understanding conflict resolution *before* building sync prevents rework.

---

### 4. **Service Workers & Network Interception**
*Why it matters fourth:* Now you're ready for *mechanics*. Service workers sit between your app and the network, letting you intercept requests and serve cached responses when offline.

**The core idea:** A service worker is a background script that can respond to network requests. You use it to: cache assets on install, serve from cache when offline, queue mutations for later sync.

**Why it comes here:** This is the *how*, not the *why*. Without the conceptual foundation (1–3), you'll copy-paste service worker code without understanding when or why to use it.

---

### 5. **Sync Strategies & Background Sync API**
*Why it matters fifth:* With storage, conflict handling, and a service worker in place, you're ready to get sophisticated about *when* and *how* to sync back to the server.

**The core idea:** You can sync eagerly (on every change), lazily (on demand), or on a schedule. The Background Sync API lets you defer sync until the network is back, even if the user closes the app.

**Why it comes last:** This is the polish layer. You can build offline support without it (just sync when the user reopens the tab). The API makes it invisible and reliable.

---

## Recommendation

**Start with 1 and 2.** Spend time on state synchronization + storage before touching service workers. Too many teams jump to service workers without a mental model for *what* they're caching and *why*, and end up with stale-data bugs.

Once you've settled on those, read up on conflict resolution for your specific app (CRUD vs. real-time vs. read-mostly all have different answers).

### Next prompt should include
- What type of web app (e.g., "collaborative document editor," "shopping cart," "analytics dashboard")
- Whether you have a preference for PWA / service workers, or are exploring all options
- Any specific pain points (e.g., "users go offline mid-transaction," "we need live updates")

This will let me pitch the 5 ideas specifically to your app's constraints.