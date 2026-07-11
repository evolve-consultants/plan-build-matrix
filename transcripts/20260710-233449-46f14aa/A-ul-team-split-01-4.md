Here's a structured way to break the tie:

**Start by identifying what's actually driving each side:**
- REST advocates: Is it "GraphQL is overengineered" or "we don't have the bandwidth"? These are different problems.
- GraphQL advocates: Are they solving real pain points (over-fetching, N+1 queries, mobile clients) or just attracted to new tech?

**Run a small experiment:**
- Build one non-critical endpoint/feature in GraphQL
- Measure what matters to your team: query efficiency, development speed, client satisfaction, operational complexity
- Set a clear success criterion before you start (not moving goalposts after)

**The honest questions:**
- Do your clients actually need what GraphQL provides? (Multiple front-ends, mobile clients, varying data needs)
- Can you afford the operational shift? (monitoring, caching, rate limiting work differently)
- Is your REST API actually a problem, or are you solving for the future?

**When REST is probably fine:**
- Simple, stable data models
- One or two client types with consistent needs
- Small team

**When GraphQL makes sense:**
- Many client types with different data needs
- You're spending time on API versioning
- Clients frequently ask for new fields/combinations

The worst outcome is migrating because half your team wanted to, then discovering you needed neither. The experiment de-risks that.

What's the actual friction your team is experiencing with REST right now?