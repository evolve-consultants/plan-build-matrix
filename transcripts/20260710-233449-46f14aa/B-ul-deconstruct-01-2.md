**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You want a ranked list of core concepts for offline support—ordered so that each one builds on the last, from "you need to understand this before anything else" to "this is the advanced stuff." This is about learning path, not implementation checklist.

<assumptions>
  <project>You have a web app (likely client-side heavy, possibly with a backend). I'm assuming it's currently online-only.</project>
  <task>You're scoping what "offline support" means by breaking it into conceptual pieces. You may be planning a rollout, evaluating feasibility, or deciding where to start learning.</task>
  <operator>You're technical enough to implement this yourself (or lead a team), but you're not yet fluent in the specific patterns and tradeoffs.</operator>
</assumptions>

### What I'm unsure of
- **Scope of "offline"**: Are we talking "works fine without internet for hours/days" or "gracefully degrades if connection drops briefly"? This changes which concepts matter most.
- **Data shape**: Is your app mostly read-heavy (fetch data once, view offline) or write-heavy (users create/edit content offline, sync later)? Very different foundational challenges.
- **User expectations**: Does your offline mode need to be invisible (seamless sync), explicit (user knows they're offline), or somewhere in between?

### Here's my recommended path

Rather than guess, I'd surface options first:

**If you want a generic ranking** (covers most offline scenarios):
1. **State synchronization** — your app needs *two* sources of truth (server, device) and logic to keep them consistent
2. **Offline detection & connectivity patterns** — knowing when you're offline vs. online, and how to handle transitions
3. **Local persistence** — where/how data lives on the device (IndexedDB, localStorage, SQLite, etc.)
4. **Conflict resolution** — what happens when the same data is edited offline and online simultaneously
5. **Sync strategies** — *when* and *how* to push changes back to the server

**If your app is read-heavy** (most content is fetched, then viewed offline):
Start with persistence, then detection, then state sync, then sync strategy, then conflict resolution.

**If your app is write-heavy** (users create/edit offline):
Start with state sync, then conflict resolution, then detection, then persistence, then sync strategy.

### Recommendation
Give me answers to the three uncertainties above (especially data shape and scope). That will let me order these five concepts in a way that actually matches your learning path, rather than a generic one.

**Or**, if you want the generic ranking now to get started, I can flesh that out immediately — just confirm that's what you're after.

### Next prompt should include
- How heavy is write traffic when offline? (Can users create/edit, or mostly just view?)
- How long do you need offline support to last? (Minutes? Hours? Days?)
- Should sync be automatic and invisible, or should users explicitly "sync when ready"?