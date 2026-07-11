Here's a structured way to work through this:

**First, understand what's actually driving each side:**
- REST advocates: What problems do they think this creates? (added complexity, learning curve, unfamiliar tooling?)
- GraphQL advocates: What specific pain points are they experiencing? (over-fetching, N+1 queries, client flexibility needs?)

Often you'll find the real issue isn't the technology itself.

**Then honestly assess:**

- **Do you have an actual problem GraphQL solves?** Over-fetching on mobile clients? Multiple client types needing different data shapes? Or is this more about "GraphQL is cool"?
- **What's the cost of switching?** Not just migration time—ongoing maintenance, team ramp-up, debugging complexity, potential performance gotchas (caching, complexity limits)
- **What's the cost of staying?** Is REST actually creating friction in daily work?

**Middle-ground options worth considering:**
- Try GraphQL for *one new service* while keeping REST elsewhere
- Build a GraphQL layer on top of existing REST (reduces migration risk)
- Improve your REST API design instead (better endpoint structure, filtering, sparse fieldsets)

**The real flag:**
If half your team is lukewarm, a full migration will be painful. You need either clearer consensus or a problem so obvious that the answer becomes obvious too.

What's the actual pain point pushing the GraphQL side? That usually tells you if this is worth the effort.