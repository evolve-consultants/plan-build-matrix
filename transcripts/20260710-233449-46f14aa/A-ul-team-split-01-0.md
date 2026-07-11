Here's a practical way to untangle this:

**First, understand what's actually driving each side:**
- What specific problems are they hoping GraphQL solves? (Over-fetching? Client flexibility? Developer experience?)
- What concerns does the other half have? (Complexity? Performance? Migration effort?)

Often these aren't really about REST vs GraphQL—they're about different problems you're trying to solve.

**Then ask yourselves:**

- **Is this a real pain point?** Are clients actually struggling with over-fetching, versioning, or API flexibility? Or does REST work fine?
- **What's the switching cost?** (rewriting, testing, learning curve, tooling)
- **What's the upside for *your* use case?** GraphQL shines for some scenarios (mobile clients, varied data needs) but isn't universally better.

**Low-risk middle grounds to consider:**
- Try GraphQL on one new service/team as a pilot
- Add a GraphQL layer alongside REST temporarily
- Just improve your REST API design (better pagination, sparse fieldsets, etc.)
- Solve the actual problem differently (e.g., if it's mobile data usage, look at compression/caching first)

**Red flags suggesting "not now":**
- Your REST API isn't actually causing problems
- Team lacks GraphQL experience and adoption would be slow
- You'd be doing this to keep up with trends rather than solve something

The worst outcome is splitting effort between two systems because the team couldn't decide. What specific problems are they pointing to?