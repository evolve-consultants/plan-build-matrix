# Offline Support: 5 Foundational to Advanced Concepts

## 1. **Client-Side Storage (Foundation)**
Understanding where and how to store data locally on the user's device. This includes localStorage, sessionStorage, and IndexedDB—the actual containers that hold your data when the server is unreachable.

## 2. **Network State Detection**
Knowing whether the user is currently online or offline, and how to respond appropriately. This involves listening to browser events and understanding connection quality, not just binary on/off states.

## 3. **Data Synchronization**
The logic for reconciling local changes with the server once connectivity returns. This includes queuing actions, deciding conflict resolution rules, and ensuring data consistency between client and server.

## 4. **Service Workers**
The underlying technology that enables offline functionality—a background script that intercepts network requests, serves cached responses, and manages background sync. This is where offline support actually *happens*.

## 5. **Advanced Sync Strategies (Most Complex)**
Sophisticated patterns like partial sync, optimistic updates with rollback, handling stale data, and designing APIs that support offline-first architecture. This requires thinking about edge cases like concurrent edits and managing user expectations.

---

**Tip:** Start by picking one storage method (#1) and network detection (#2) before building anything. Many teams jump to Service Workers before understanding what data they actually need to persist.