This is worth deciding thoughtfully rather than by vote. Some honest questions to narrow it:

**Diagnose the actual pain point:**
- Is the push coming from "GraphQL is modern" or from specific problems? (over-fetching data, multiple endpoint calls, versioning headaches?)
- Are those real bottlenecks for your users or developers, or theoretical?

**Reality-check the cost:**
- GraphQL isn't zero-effort—caching gets harder, query complexity needs guardrails, debugging differs
- Migration means rewriting clients, not just the backend
- You need someone who knows GraphQL well; "learning on production" rarely goes well

**Honest scenarios where it's worth it:**
- Multiple clients with different data needs (web, mobile, third-party)
- Heavy over-fetching or N+1 query problems you've measured
- Rapid iteration on client data requirements

**Scenarios where it's probably not:**
- One primary client that works fine now
- Your REST API is already reasonably designed
- Team doesn't have GraphQL experience and you're busy

**A middle path:**
Instead of big-bang migration: add GraphQL as an *additional* API layer for new features or specific clients. Proves value without forcing the whole team to commit. If it's genuinely better, adoption spreads naturally.

What's actually frustrating your team right now about the current API? That'll tell you if this is solving a real problem.