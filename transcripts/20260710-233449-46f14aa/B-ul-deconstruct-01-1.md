**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You want a learning path — 5 core concepts about offline support, ordered so each one builds on the previous, so you can understand the landscape before diving into implementation.

<assumptions>
  <project>You have an existing web app (client-server architecture, likely JavaScript-based, though you haven't specified the tech stack)</project>
  <task>You're evaluating offline support as a feature or capability, not yet committed to building it</task>
  <operator>You're comfortable with web fundamentals but may not have deep experience with service workers, caching strategies, or sync patterns</operator>
</assumptions>

### What I'm unsure of
- Whether you want this ordered by *logical dependency* (what you need to know first to understand the next thing) or *implementation complexity* (easiest to hardest to build). I'm assuming logical dependency.
- Whether you care equally about conceptual understanding vs. practical "how do I actually do this?" knowledge. If it's the latter, I should weight the path toward tools and patterns.
- Whether your app is real-time/collaborative (like Figma) or transactional (like a todo app or form submission). The priorities shift.

### Here's the foundational-to-advanced sequence:

1. **The offline/online spectrum** (foundational)
   - Offline isn't binary. Understand: read-only offline, deferred writes, real-time sync, conflict resolution. Most apps don't need full offline parity. What *subset* of your app makes sense offline?

2. **What data persists where** (foundational)
   - The browser has multiple storage layers: localStorage (small, sync, unstructured), IndexedDB (large, async, queryable), Service Worker cache (HTTP responses only). Each has different tradeoffs. You need to know which tool fits which problem.

3. **Service Workers and the request lifecycle** (core)
   - Service Workers intercept network requests and let you decide what happens: serve from cache, fetch from network, or fail gracefully. This is the mechanism that makes offline work. You don't need to build one, but you need to understand what they do and why they're necessary.

4. **Sync strategies and conflict handling** (advanced)
   - Once users can write offline, writes collide with server state. You need a strategy: optimistic updates (assume it works), pessimistic queuing (wait for confirmation), last-write-wins, or multi-way merge. Each has failure modes. Pick the one that matches your app's semantics.

5. **State machine and edge cases** (advanced)
   - Offline support multiplies states: online, transitioning, offline, reconnecting, conflict, stale. Your app needs to move through these predictably. This is less about the tech and more about *thinking through* what happens when the network flickers, the user closes the tab mid-sync, or two devices write simultaneously.

### Why this order?
1 and 2 are definitional — you need these before you can make a choice. 3 is the mechanism that makes everything else possible. 4 and 5 are the hard problems that emerge *after* you've built the mechanism.

### Next prompt should include
- What type of offline makes sense for your app? (read-only, deferred writes, real-time collaboration?)
- Do you want me to expand any of these 5 into a deeper walkthrough?
- Should I include a quick decision tree: "do you actually need offline support, or would something simpler suffice?"