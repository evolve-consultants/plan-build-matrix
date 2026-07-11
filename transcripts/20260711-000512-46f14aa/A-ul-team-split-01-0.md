# Deciding on REST vs GraphQL

Before picking a side, it's worth figuring out *why* your team is split—usually these debates hide different underlying concerns that are worth surfacing explicitly.

## Questions to ask first

**What problem is GraphQL actually solving for you?**
- Are clients over-fetching or under-fetching data?
- Do you have many different client types (mobile, web, third-party) with different data needs?
- Are you drowning in endpoint proliferation or versioning headaches?

If you can't point to concrete pain points, that's a signal the push might be more about resume-building or chasing trends than solving a real problem—worth naming that directly in the discussion.

**What's the cost side?**
- Do you have GraphQL experience on the team, or is this a learning curve on top of a migration?
- How will this affect caching (REST's HTTP caching is simpler; GraphQL often needs more work)?
- What's your API surface size? Small APIs rarely benefit enough to justify the switch.

## A practical way to resolve the disagreement

1. **Write down the actual pain points** people are experiencing with REST today. Get specifics, not vibes.
2. **Map each pain point** to whether GraphQL solves it, whether it's solvable in REST too (e.g., using sparse fieldsets, better endpoint design), and whether it's even a "must fix now" problem.
3. **Consider a middle path**: add GraphQL as a layer/gateway in front of existing REST services for a specific use case (e.g., a mobile client that needs flexible queries) rather than a full rip-and-replace. This lets you evaluate real benefits with contained risk.
4. **Timebox a spike**: have someone prototype the highest-value use case in GraphQL and demo it. Concrete code often ends debates faster than opinions do.

## A caution

Full migrations driven by internal disagreement (rather than clear customer/business pain) often stall halfway, leaving you maintaining *two* API paradigms indefinitely — probably the worst outcome. If you go for it, be decisive about scope and timeline, not open-ended.

What's actually driving the push on your team — is it a specific pain point, or more of a general "GraphQL is better" sentiment? That might help narrow down the right move.