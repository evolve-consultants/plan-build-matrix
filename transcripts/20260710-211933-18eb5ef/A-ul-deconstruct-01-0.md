# Offline Support: 5 Key Ideas (Foundational → Advanced)

## 1. **The Network Gap Problem**
Understand that users lose connectivity unpredictably, and your app currently fails when the network is unavailable. You need to distinguish between what *must* work offline (core features) versus what can gracefully degrade (nice-to-haves).

## 2. **Local Storage Mechanisms**
Learn how browsers store data locally: **localStorage** (simple key-value, limited size), **IndexedDB** (structured, large-scale), and **Service Workers** (enable caching). Pick the right tool based on your data volume and query complexity.

## 3. **State Synchronization**
Recognize that offline and online represent two diverging versions of your data. You need a strategy to reconcile changes made offline with server state when connectivity returns—deciding what to keep, merge, or discard.

## 4. **Service Workers & the Request Interception Layer**
Master how Service Workers act as a proxy between your app and the network. They intercept requests, serve cached responses when offline, and queue requests for later—this is the engine that makes offline work seamless.

## 5. **Conflict Resolution & Data Consistency**
Handle the hard problem: when offline and online changes conflict, which version wins? This requires thinking about operational transformation, last-write-wins strategies, or custom business logic to maintain data integrity across devices.

---

**Start with #1-2, implement #3-4, then architect #5 based on your data model's needs.**