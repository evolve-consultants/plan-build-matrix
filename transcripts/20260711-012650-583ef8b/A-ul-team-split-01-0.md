This is a genuinely legitimate split. Both sides have real points:

**The "GraphQL makes sense" case:**
- Clients stop over-fetching and under-fetching data
- Single endpoint beats maintaining 20 REST routes
- Better for mobile/bandwidth-constrained clients
- Strong typing in schema can catch bugs early

**The "stick with REST" case:**
- REST is simpler to learn and reason about
- Caching (HTTP layer, CDNs) is more straightforward
- You're probably not hitting the pain points yet
- Migration cost is real, not theoretical

**Better question to ask first:** What actual problems are you trying to solve?

- Are clients frequently requesting data from multiple endpoints?
- Do you have mobile clients struggling with bandwidth?
- Is API maintenance consuming significant time?
- Are you building something totally new vs. migrating existing?

**A pragmatic path forward:**
1. **Timeline check**: Do you have shipping pressure? REST is faster to iterate with.
2. **Pilot, don't flip**: New service? Try GraphQL there. Keep REST running in parallel.
3. **Measure real friction**: Before big migration, log what queries your clients actually make. Is it wasteful?
4. **Consider the middle ground**: Better REST practices (sparse fieldsets, better filtering) might solve 70% of complaints for 5% of effort.

The worst outcome isn't choosing wrong—it's having half the team resentful about either choice. What's actually broken in your current setup?