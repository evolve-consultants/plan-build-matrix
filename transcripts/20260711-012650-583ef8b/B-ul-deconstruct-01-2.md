**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You want a foundational-to-advanced breakdown of the core concepts required to implement offline support in a web app—the mental models and technical ideas you need to grasp before building.

<assumptions>
  <project>This is a web app (client-side JavaScript), likely with a backend. I'm assuming you don't have offline support yet.</project>
  <task>You're trying to build a mental model before diving into implementation, so you can make good architectural decisions and understand trade-offs.</task>
  <operator>You have web development experience but may be new to offline-first patterns and service workers.</operator>
</assumptions>

### What I'm unsure of
- Whether you care more about read-only offline access (view cached data) or read-write (queue mutations while offline)
- Whether the app is real-time collaborative or single-user
- Your tolerance for complexity vs. feature completeness (offline support has many levels)

### The five ideas, foundational to advanced

| # | Idea | Why it matters |
|---|---|---|
| **1** | **Network as fallback, not requirement** — Your app must function without assuming the network exists. The network is an optional enhancement, not the foundation. | This mindset flip changes everything. Without it, offline support feels like a patch; with it, it's an architectural principle. All other decisions flow from here. |
| **2** | **Local state and sync, not real-time reflection** — Changes must work against local data first (IndexedDB, SQLite, local storage), then sync to the server asynchronously. The UI responds instantly to local changes; the server catches up later. | This breaks the "submit form, wait for server response" mental model. You need to think in terms of eventual consistency and conflict resolution. |
| **3** | **Service Workers as the offline gateway** — A service worker intercepts network requests and decides: cache-first, network-first, or stale-while-revalidate. It's the layer that makes offline possible. | Without understanding what a service worker is and how it sits between your app and the network, offline support is mysterious. This is the *how*, not just the *what*. |
| **4** | **Conflict resolution and versioning** — When offline changes collide with server updates (user edits locally, someone else edits on the server), you need a strategy: last-write-wins, operational transforms, or domain-specific logic. You must version your data. | This is where offline-first gets hard. Simple caching is easy; handling conflicts is not. You need a principled approach or your app will corrupt data silently. |
| **5** | **Replication and sync protocols** — Tools like CRDTs (Conflict-free Replicated Data Types) or event logs let you reason about syncing as replication, not just "send changes and hope." Knowing whether you need client-side CRDT libraries or server-side event sourcing changes the whole architecture. | This is the advanced layer where offline support becomes systematic. Most apps don't need CRDTs, but understanding when and why you might need them is the mark of informed design. |

### Recommendation
Start with **1 and 2** — they're philosophical. Get comfortable with the idea that your app lives offline-first before you touch Service Workers. Then tackle **3** as the tactical implementation layer. **4 and 5** become relevant only when you try to sync and realize "oh, two versions of the truth exist."

### Next prompt should include
- Your offline use case: read-only (just viewing data offline) or read-write (creating/editing offline)?
- Whether data needs to sync across multiple devices or just survive a network blip on one device
- Whether you want a gentle introduction (step-by-step tutorial style) or a deeper architectural walkthrough