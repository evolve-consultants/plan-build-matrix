**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You want a learning path — 5 core concepts that build on each other, ordered so you can tackle foundational ideas before advanced ones. This is meant to guide what you study before or while implementing offline support.

<assumptions>
  <project>You have a web app (likely client-server architecture); you're considering Service Workers, local storage, or sync mechanisms as part of the solution</project>
  <task>You want to understand offline support deeply enough to make architectural decisions and implement it competently, not just follow a tutorial</task>
  <operator>You have web development experience but may not have worked with offline patterns or progressive web app infrastructure before</operator>
</assumptions>

### What I'm unsure of
- Whether you're building a new app or retrofitting offline into an existing one (affects priority of certain concepts)
- Your risk tolerance for data loss or eventual consistency issues
- Whether you need to support all browsers or just modern ones

### Here's the foundational stack, ordered

1. **Network state and the offline/online distinction** (most foundational)
   - How browsers detect connectivity; what "offline" actually means
   - Why it's not binary — you can have a socket but no DNS, have internet but no backend
   - Why you can't rely on a single connectivity check

2. **Service Workers as the interception layer**
   - What a Service Worker is and why it exists (runs separately from your page, can intercept requests)
   - Lifecycle (install, activate, the difference between functional and cache-first strategies)
   - Why this is the *only* way to truly intercept requests in modern browsers
   - This is the mechanism that makes offline possible; everything else builds on it

3. **Storage strategies and data persistence**
   - The differences between localStorage, IndexedDB, and in-memory caches
   - Why IndexedDB matters for offline (localStorage is too small and synchronous)
   - Read/write patterns and capacity limits
   - This is where your data actually lives when offline

4. **Conflict resolution and eventual consistency**
   - What happens when the user edits offline and the server has changed the same data
   - The difference between optimistic updates, pessimistic updates, and conflict merging
   - Why you can't avoid this decision — every app makes it implicitly
   - This is where offline gets *hard*

5. **Sync patterns and background tasks** (most advanced)
   - When requests fail, how do you queue them and retry later?
   - Background Sync API (if supported) vs. manual retry-on-reconnect patterns
   - Ordering, idempotency, and what happens if a sync job fails mid-way
   - This is where you coordinate the offline and online states back together

### Recommendation
Start with **1 and 2** — understand the problem space and the tool that solves it. Once you can mentally model "what happens when a request is made offline and the Service Worker intercepts it," you're ready for 3. Concept 4 is critical for your design, so tackle it before writing much code. Concept 5 is the implementation detail that follows from 4.

### Next prompt should include
- Whether you're building new or retrofitting (changes the order slightly)
- Any specific constraints (browser support, data sensitivity, user expectations around offline)
- If you want me to go deep on any one concept now, or if you'd rather come back with specific questions as you hit each layer