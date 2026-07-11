# Adding Offline Support to Web Apps: 5 Key Ideas

## 1. **Service Workers as the Foundation**
The browser mechanism that intercepts network requests and runs in the background. You need to understand that Service Workers sit between your app and the network, allowing you to decide what happens when the user is offline—whether to serve cached content or show an error.

## 2. **The Cache Storage API**
A dedicated storage system (separate from localStorage) designed specifically for caching assets. Understand that you strategically store different types of content (HTML, CSS, JS, API responses) with versioning so you can update and manage what's available offline.

## 3. **Sync Strategies: What to Cache vs. What to Sync**
The decisions about which data and features work offline versus which require a connection. You need to distinguish between read-only content (cache-first for static assets) versus user-generated data (store locally, sync when reconnected).

## 4. **Conflict Resolution and Data Consistency**
When users make changes offline and reconnect, their local changes might conflict with server updates. You need to handle scenarios like duplicate submissions, stale data, and deciding whose version wins when conflicts occur.

## 5. **Background Sync & Notification Strategies**
Advanced patterns like queuing failed requests to retry automatically when reconnected, and using Web Push to notify users about sync status. This requires understanding service worker lifecycle and user expectations around asynchronous updates.

---

Each level builds on the previous—you can't effectively resolve conflicts without understanding sync strategies, and you can't implement those without knowing the Cache API.