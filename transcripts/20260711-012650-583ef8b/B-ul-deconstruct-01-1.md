**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You want a learning roadmap for offline support — the core concepts ranked by dependency, so foundational ideas come first and each one builds on what came before.

<assumptions>
  <project>You have an existing web app (client-server architecture assumed); I don't know its tech stack, data model complexity, or how much state syncing is involved</project>
  <task>You're preparing to add offline capability and want to study the right concepts in the right order before implementation</task>
  <operator>You're technically capable but may not have built offline systems before; you want conceptual clarity, not a tutorial</operator>
</assumptions>

### What I'm unsure of
- **Stack specificity**: Are you using a framework with offline helpers (e.g., Expo, Next.js offline plugins) or building from scratch? This changes whether some concepts are your responsibility or delegated.
- **Scope of offline**: Does "offline" mean read-only (cached data), read-write (queued mutations), or both? Full sync or eventually consistent?
- **Data sensitivity**: Do you have regulatory or security constraints around cached data on the device?

---

### Here's the foundational-to-advanced sequence:

1. **Cache strategy and stale-while-revalidate patterns**
   - *Why it's foundational*: You can't serve offline content without storing it locally first. Understanding *when* to cache, *how long* to keep it, and *how to refresh* it is prerequisite to everything else.
   - *Core concept*: Network request → cache for future use; offline mode reads from cache. TTL, invalidation, freshness.

2. **Service Workers and background sync**
   - *Why it comes next*: Once you understand caching, you need a mechanism to intercept network requests and manage offline/online transitions. Service Workers are the plumbing.
   - *Core concept*: Runs on a separate thread; can intercept requests; can queue work (Background Sync API) for when connection returns.

3. **State management and mutation queueing**
   - *Why it's intermediate*: Read-only offline is simple; the moment users can *write* offline, you need to queue mutations and replay them when online.
   - *Core concept*: Capture user actions offline → store them locally → send when connection restored. Order matters. Conflicts possible.

4. **Conflict resolution and eventual consistency**
   - *Why it's advanced*: Once mutations are queued, you need a strategy for when the queued action conflicts with server state (user edited offline, server changed the same field meanwhile).
   - *Core concept*: Last-write-wins, operational transforms, CRDTs, or app-specific merge logic. Each has tradeoffs.

5. **Sync state management and user feedback**
   - *Why it's most advanced*: The system now has three states (offline, syncing, online) with different UI implications. You need to track sync progress, communicate uncertainty, and handle partial failures gracefully.
   - *Core concept*: "Syncing…" badges, optimistic UI updates, retry strategies, error recovery, and telling the user when something failed to sync.

---

### Recommended path
Start with 1 and 2 in parallel (they're tightly linked). Master those before tackling 3. Then 4 and 5 flow naturally, but 4 is the pivot point — once you understand it, you understand the cost of offline support.

### Next prompt should include
- Confirmation of your stack and offline scope (read-only or read-write?)
- Whether you want to dive into one of these concepts now or continue mapping the problem space
- Any regulatory/security constraints I should keep in mind