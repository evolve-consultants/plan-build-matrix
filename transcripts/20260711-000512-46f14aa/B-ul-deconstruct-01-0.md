**Operating from: Bottom-Right (Build + Quality)**

### Confirming before I proceed
- I'm assuming "our web app" means a browser-based app (not React Native/Flutter), so this covers Service Worker–based offline patterns, not native mobile offline APIs.
- I'm assuming you want framework-agnostic concepts (the "why" and "what"), not framework-specific implementation (e.g., not "how Workbox works in your Next.js setup") — this is prep for later build decisions, not a tutorial.
- I'm assuming "understand first" means you want the conceptual dependency chain — each idea below assumes the ones before it.

If any of these are off (e.g., you're actually building a hybrid/native app, or you want framework-specific detail), let me know and I'll adjust.

### The artifact

**1. Network state isn't binary — it's a spectrum you must detect and react to**
Before touching any offline tech, internalize that "offline" includes flaky, slow, and intermittent connections, not just fully disconnected. The `navigator.onLine` API and `online`/`offline` events are unreliable signals on their own (a device can report "online" while requests still fail). Foundational mental shift: design for "assume any request can fail or hang," not "detect offline and branch."

**2. Service Workers + the Cache API are the interception layer**
This is the core mechanism everything else builds on. A Service Worker sits between your app and the network, letting you intercept `fetch` requests and decide: serve from cache, go to network, or some hybrid. The three canonical strategies to learn (in order of complexity):
- Cache-first (fast, but can go stale)
- Network-first (fresh, but slow/fails offline)
- Stale-while-revalidate (serve cached immediately, update cache in background)

Nothing else on this list works without understanding this interception point.

**3. Persistent storage for actual app data (IndexedDB, not just cached responses)**
The Cache API stores network *responses* (HTML, JSON, assets). But real offline support usually means the app's *data* — user input, app state, records — needs to persist and be queryable offline too. That's IndexedDB (or a wrapper like Dexie). This is a distinct concept from caching: caching preserves what the server sent; this preserves what the user is doing.

**4. Write queuing and background sync (handling offline mutations)**
Once users can *read* offline, the harder problem emerges: what happens when they try to *write* (submit a form, save an edit) while offline? This requires queuing the intended action locally, then replaying it when connectivity returns (Background Sync API or a custom retry queue), plus deciding how to handle conflicts if the server state changed in the meantime. This is more advanced because it touches server-side reconciliation, not just client caching.

**5. Communicating state and degrading gracefully (UX layer)**
The most advanced piece, because it requires the first four to already work: how do you tell the user they're offline, that an action is queued, or that data might be stale? This includes optimistic UI (show the change immediately, assuming the sync will succeed), offline indicators, and deciding which features simply *don't* work offline vs. which degrade gracefully. Get this wrong and users won't trust the offline mode even if the plumbing is solid.

*(Misread the scope? Say so — if this is actually about a native/hybrid app or you want framework-specific detail, I'll re-scope.)*