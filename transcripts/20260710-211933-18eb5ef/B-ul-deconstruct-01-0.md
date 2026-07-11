**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You want a foundational-to-advanced breakdown of offline support concepts so you can understand the landscape before building. This is a learning map, not an implementation plan yet.

<assumptions>
  <project>You have a web app (tech stack unknown); offline support is a new capability</project>
  <task>You're building conceptual fluency so you can make informed decisions about *which* offline patterns to implement and *why*</task>
  <operator>You want to learn, not just execute. You probably don't have offline experience yet</operator>
</assumptions>

### What I'm unsure of
- Whether you're optimizing for read-heavy, write-heavy, or mixed workloads
- Whether your app is realtime (multiplayer, live updates) or transaction-based
- Whether offline means "no network for 5 minutes" or "days without connection"
- Whether data freshness matters more than availability

These affect which concepts matter most. But I can give you the universal foundation regardless.

---

## The 5 Concepts (Foundational → Advanced)

### 1. **State Sync: The Core Problem**
*Why:* Everything else is a solution to this.

You have two sources of truth: client and server. When offline, the client keeps working but falls out of sync. When online, you have to merge them back. That merge is the hard part — not the storage, not the detection. 

**Why it's foundational:** Until you understand that offline isn't "pretend the server doesn't exist," you'll build something that breaks the moment someone edits something offline and online simultaneously.

---

### 2. **Optimistic Updates vs. Queuing**
*Why:* These are the two primary patterns for handling user actions offline.*

- **Optimistic**: assume the server will say yes, update the UI immediately, then verify later. If it fails, you have to undo.
- **Queuing**: store the action, show "pending," send it when online, then update the UI.

Different tradeoffs: optimistic feels fast but risks UI/server mismatch. Queuing is safer but feels slower.

**Why it matters:** Your choice here cascades into your architecture. Pick wrong and you're retrofitting later.

---

### 3. **Local Storage vs. Service Workers vs. IndexedDB**
*Why:* You need somewhere to store data and logic when offline.*

- **LocalStorage**: simple key-value, ~5-10MB, synchronous (blocks the thread)
- **IndexedDB**: proper database, ~50MB+, asynchronous, queryable
- **Service Workers**: run independently of your page, intercept network requests, enable background sync

Most offline apps use IndexedDB (storage) + Service Worker (network layer).

**Why it's mid-level:** This is where theory meets implementation. You need to know what tool fits the job before you pick one.

---

### 4. **Conflict Resolution Strategies**
*Why:* When client and server both made changes while offline, which one wins?*

- **Last-write-wins**: server version overwrites (loses client work, but simple)
- **Client-wins**: client version overwrites (can lose server updates, risky)
- **Merge**: intelligently combine both (complex; requires domain knowledge)
- **Prompt user**: "Which version do you want?" (safe but interrupts flow)

Real apps use different strategies for different fields. A timestamp gets last-write-wins. A shopping cart might merge. A name edit might prompt.

**Why it's advanced:** Requires you to think about data semantics, not just mechanics.

---

### 5. **Eventual Consistency & Partial Sync**
*Why:* Not everything needs to sync. Not everything can sync immediately.*

You can't always keep everything in sync everywhere. So you define:
- **What syncs**: maybe only your data, not everyone's
- **When**: on-demand, on a schedule, on connection restore, or continuously
- **What's acceptable**: is it okay for this user to see stale data for 10 seconds?

This is about trading off freshness, bandwidth, battery, and complexity.

**Why it's the capstone:** Once you've built the basics, this is what separates "works offline" from "works offline *well*." It's about intentional design, not just fallback behavior.

---

## Recommended path

Start by building mental models of concepts 1–2. They're universal. Then, *before* you write code, figure out your answer to #4 (conflict resolution) because it should shape your storage choice (#3). #5 emerges naturally once you're testing real offline scenarios.

## Next prompt should include
- Your app's primary use case (read-heavy, write-heavy, realtime?)
- How long offline matters (minutes, hours, days?)
- Whether multiple users can edit the same data
- Whether you've picked a tech stack yet (React, Vue, etc.?)

Once I know those, I can give you a recommended pattern (e.g., "optimistic updates + IndexedDB + last-write-wins" or something more suited to your constraints).