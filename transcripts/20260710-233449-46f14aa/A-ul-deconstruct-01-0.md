# Offline Support: 5 Key Ideas (Foundation → Advanced)

## 1. **The Network-Aware Application Model**
Your app needs to acknowledge that connectivity is unreliable and intermittent, not binary. Users aren't simply "online" or "offline"—they're on spotty WiFi, switching between networks, or losing signal. Design assuming the network can fail at any moment.

## 2. **Local Data Storage (The Cache Layer)**
You need somewhere on the user's device to persist data beyond memory. Service Workers combined with IndexedDB or SQLite (depending on your platform) let you store meaningful amounts of application data locally so it survives page refreshes and app restarts.

## 3. **Request Queuing & Sync Strategy**
When offline, user actions can't reach your server immediately. You'll need to queue those requests and replay them when connectivity returns. This includes deciding what to queue, in what order, and how to handle conflicts when the server state has changed.

## 4. **Conflict Resolution & Data Reconciliation**
When the device was offline, the user might have changed data that was also modified server-side. You need a strategy to merge these changes intelligently (last-write-wins, user prompts, field-level merging, etc.) rather than just overwriting one version.

## 5. **Eventual Consistency & Optimistic UI**
Rather than waiting for server confirmation, show users their changes immediately while syncing in the background. Accept that what's displayed locally might briefly diverge from server truth. This requires robust error handling and rollback mechanisms when sync fails.

---

**Quick dependency note:** Each level builds on the previous—you can't do smart conflict resolution without a queue, and you can't have a queue without local storage.