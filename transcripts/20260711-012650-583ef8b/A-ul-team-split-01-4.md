Before making a big switch, I'd step back and ask: **what problem are you actually trying to solve?**

GraphQL isn't universally better—it trades different tradeoffs. Some legitimate reasons to consider it:

- **Multiple clients with different data needs** (web, mobile, third-party integrations requesting different field subsets)
- **Over-fetching is a real pain point** you're currently experiencing
- **Query complexity** your REST endpoints have become (lots of nested relationships requiring multiple calls)
- **Strong developer experience** needs for internal tools/partners

Reasons the skepticism might be justified:
- **REST works fine** for your actual use cases
- **Operational complexity** increases (caching, query monitoring, rate limiting are harder)
- **Team learning curve** is real if you're not experienced with it
- **Simple data shapes** don't benefit much from GraphQL's flexibility

**What I'd actually do:**

1. **Get specific**: Have the pro-GraphQL side articulate concrete problems REST causes *today*, not theoretical ones
2. **Run a small experiment**: Build one new feature or endpoint in GraphQL on a side project. See if the developer experience improvement justifies the overhead
3. **Consider the middle ground**: Maybe GraphQL for public APIs but REST internally, or just better REST design (proper pagination, sparse fieldsets)
4. **Check the real costs**: Who maintains this? What's your ops story? Can you actually support it?

The worst outcome is switching because it's trendy, then resenting the complexity. What's driving the push from your team?