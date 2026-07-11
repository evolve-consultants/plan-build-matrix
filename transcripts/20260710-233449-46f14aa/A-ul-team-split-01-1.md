Before deciding, I'd separate the **actual problem** from the solution being proposed.

**Ask first:**
- What specific pain points are people experiencing? (Over-fetching data? Versioning issues? Mobile bandwidth? N+1 queries?)
- Is GraphQL actually the right fix, or are there simpler solutions?

**GraphQL makes sense if you have:**
- Multiple clients with different data needs (web, mobile, third-party integrations)
- Significant over-fetching in your current API
- The team capacity to maintain it properly
- A frontend team that will actually benefit

**GraphQL doesn't solve:**
- Poor database performance
- Authentication/authorization complexity (just shifts it)
- The need for good API design discipline

**A practical middle path:**
1. **Time-box a spike** (1-2 weeks). Have the interested half prototype a small GraphQL endpoint alongside REST
2. **Measure against real problems** — does it actually reduce bandwidth? Simplify the client code? Decrease requests?
3. **Make a data-driven call** rather than tribal preference

**Common mistake:** Teams adopt GraphQL for architectural purity, then find they've just traded REST problems for N+1 queries and complexity in other places.

If it's genuinely splitting the team and not solving a concrete problem, staying with REST + incremental improvements is often the more pragmatic call. But if there's real friction that GraphQL would fix, a low-risk proof-of-concept settles it quickly.

What's the actual pain point people are trying to solve?