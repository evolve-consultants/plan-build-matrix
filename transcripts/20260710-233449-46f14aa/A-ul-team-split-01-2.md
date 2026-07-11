This is worth deciding on actual tradeoffs rather than letting it become a philosophical split. Consider:

**GraphQL makes sense if you have:**
- Multiple client types with different data needs (web, mobile, internal tools)
- Over-fetching problems causing real performance issues
- Frequent API changes that frustrate client teams
- Complex nested relationships clients regularly need

**REST is fine if:**
- Your API is mostly simple CRUD with predictable access patterns
- Clients are homogeneous (one web app, say)
- You'd migrate everything at once (partial migration gets messy)
- Your team knows REST well and GraphQL would be learning-heavy

**A practical next step:**

1. **Audit current pain points** - Have the "waste of time" camp list specific problems. "Clients keep asking for changes" is real; "GraphQL is trendy" isn't.

2. **Prototype on one feature** - Not a full migration. Build it in GraphQL, see if it actually solves the problems you identified. This kills speculation.

3. **Cost it honestly** - Implementation, learning curve, operational complexity (caching, monitoring, query analysis), maintenance burden.

The worst outcome is migrating because half your team wanted to, then discovering it doesn't solve your actual problems while adding complexity.

What specific frustrations is the pro-GraphQL camp pointing to right now?