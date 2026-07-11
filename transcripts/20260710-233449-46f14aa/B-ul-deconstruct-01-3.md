**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You want me to break down offline support into 5 core concepts ordered from foundational to advanced, so you can build conceptual understanding before implementing. This is about knowledge prerequisites, not implementation steps.

<assumptions>
  <project>You have an existing web app (frontend + backend); I'm assuming typical SPA architecture but not whether you're using a framework or which one</project>
  <task>You want to understand offline support well enough to make architectural decisions or plan an implementation</task>
  <operator>You're technical enough to code but may not have worked with offline patterns before</operator>
</assumptions>

### What I'm unsure of
- Whether you care most about read-only offline (viewing cached data) or read-write offline (queuing mutations)
- Whether you need to support sync across multiple devices
- Whether this is for a new feature or retrofitting an existing app

### Here's my deconstruction (ordered foundational → advanced):

1. **State synchronization as the core problem** (foundational)
   - Offline isn't about "no internet" — it's about managing two diverging copies of state: one on the client, one on the server
   - Understanding that sync is fundamentally a data consistency problem, not a UI problem

2. **Local persistence mechanisms** (foundational → intermediate)
   - Where the client stores data so it survives page reloads: localStorage, IndexedDB, SQLite.wasm
   - Trade-offs: localStorage is simple but limited; IndexedDB is powerful but complex; what fits your data volume?

3. **Request queuing and replay** (intermediate)
   - When offline, you can't send mutations to the server immediately
   - The client must queue them locally, then replay them when the connection returns
   - This includes ordering guarantees, deduplication, and handling failures on replay

4. **Conflict resolution** (intermediate → advanced)
   - What happens when the server state changed while you were offline (someone else edited the same document)?
   - You need a strategy: last-write-wins, manual merge, three-way merge, operational transformation, CRDT
   - Each has different complexity and correctness guarantees

5. **Eventual consistency and user expectations** (advanced)
   - You can no longer guarantee the user sees "the truth" at any moment
   - You need to communicate uncertainty: "pending," "synced," "conflict," "failed"
   - This changes how you design UX, error handling, and what guarantees you can make to users

### Recommended path
Start by clarifying **whether you need read-only or read-write offline** — that changes which concepts matter most. Read-only offline is about #1 + #2. Read-write offline requires #3 and #4. Then work through them in order.

### Next prompt should include
- Read-only, read-write, or both?
- Rough data volume (KB, MB, GB)?
- Whether you're adding this to an existing app or designing from scratch
- Then I can generate a more specific learning sequence or architecture sketch