# Adding Offline Support: 5 Key Ideas (Foundational → Advanced)

## 1. **The Client-Server Problem**
Your web app normally relies on a server to fetch data and save changes. Offline support means your app must work *without* that connection—so you need to understand what happens when the network disappears, and that your app needs local storage to survive without it.

## 2. **Local Data Storage**
You need somewhere on the user's device to keep data when offline. The main options are:
- **LocalStorage** (simple key-value, limited size)
- **IndexedDB** (complex structured data, much larger)
- **SQLite** (via libraries like sql.js)

Choose based on your data complexity and volume.

## 3. **Detecting and Handling Network State**
Your app must know when it's online/offline and switch behavior accordingly. This involves listening to browser events (`online`/`offline`), gracefully handling failed requests, and queuing actions for when connection returns—not just crashing or hanging.

## 4. **Data Synchronization Strategy**
When the user comes back online, you need a plan to reconcile local changes with the server. Decisions include:
- What gets synced first (priority)?
- How do you handle conflicts (user changes vs. server updates)?
- Do you sync immediately or let the user review changes first?

## 5. **Conflict Resolution & Eventual Consistency**
This is where it gets tricky: the user edited something offline, the server changed it too, and now you have conflicting versions. You need a strategy—last-write-wins, user-decides, operational transformation, or CRDT approaches—and accept that perfect consistency might not be possible immediately.