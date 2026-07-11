**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You want me to break down offline support into 5 conceptual building blocks, arranged from fundamentals to advanced, so you can learn them in sequence before implementing.

<assumptions>
  <project>You have a web app (likely browser-based) that currently requires network connectivity. You're planning to add offline capability.</project>
  <task>You want to understand the conceptual landscape before diving into implementation — to know what you're working toward and why each piece matters.</task>
  <operator>You're comfortable with web fundamentals but may not have worked with Service Workers, sync APIs, or offline patterns before. You want conceptual clarity, not a tutorial.</operator>
</assumptions>

### What I'm unsure of
- Whether your app is a traditional SPA (React/Vue/Angular), a server-rendered app, or a hybrid
- Which offline features matter most to you: read-only fallback, draft creation, full sync, or something else
- Whether you care about offline-first architecture or just graceful degradation when network fails

### Here are the five ideas, foundational to advanced:

| # | Idea | In one sentence |
|---|---|---|
| **1** | **Network as a degraded state, not a binary** | Your app must assume connectivity will fail mid-interaction and handle partial or stale data gracefully. |
| **2** | **The Service Worker: your offline intermediary** | A JavaScript worker that runs independently of your page, intercepting network requests so your app can serve cached responses when offline. |
| **3** | **Storage strategies: where data lives offline** | You must choose what to cache (entire pages? API responses? just UI assets?) and where to keep it (cache API? IndexedDB? localStorage?). |
| **4** | **Conflict resolution and eventual consistency** | When users make changes offline and come back online, those changes must sync without overwriting others' work — requiring a merge strategy. |
| **5** | **Sync queuing and background sync** | Store pending actions offline, then replay them reliably when connectivity returns — either by polling or by using Service Worker APIs that let the browser batch requests. |

### Recommended path
Start with **ideas 1–3** first. They're conceptually clean and enough to build read-only offline fallback. Master those before tackling **4–5**, which are where most teams hit complexity and learn by doing.

### Next prompt should include
- Which offline features matter most to your use case (read-only, drafts, full sync?)
- What tech stack you're using
- Whether you want me to dive deep into any of these five ideas, or move toward implementation