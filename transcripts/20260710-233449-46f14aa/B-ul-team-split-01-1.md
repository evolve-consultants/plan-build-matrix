**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
Your team is split on whether to migrate from REST to GraphQL. You want a framework for deciding whether to make the move, not just a pros-cons list.

<assumptions>
  <project>You have an existing REST API in production serving real clients. The codebase is mature enough that migration is a non-trivial undertaking.</project>
  <task>You're trying to resolve team disagreement and make a defensible decision, not just pick a side.</task>
  <operator>You have decision-making authority but want to ground it in something more concrete than opinion.</operator>
</assumptions>

### What I'm unsure of
- **What problem is driving the GraphQL interest?** (Over-fetching? N+1 queries? Mobile client needs? Developer experience?) The real issue hiding in the debate matters more than the technology.
- **What's the current pain?** Are clients actively hitting limitations of REST, or is this theoretical?
- **Team skill distribution.** Do you have people who know GraphQL well, or is this learning-curve overhead?
- **Scale and complexity.** How many endpoints? How many client types consuming your API?
- **Risk tolerance.** Is this a "nice to have" or does it block something critical?

### Three decision frames

**Frame A: Follow the problem, not the technology**
Before debating GraphQL vs. REST, list the specific problems clients or developers are hitting. "We have to make 7 calls to get user profile with posts and comments" is concrete. "GraphQL is more modern" is not. If REST solves the actual problem cheaper, stop. If the problem is real and big, *then* ask whether GraphQL is the right fix.

**Frame B: Cost-benefit at your scale**
GraphQL is worth it when:
- You have multiple client types with genuinely different data needs (web, mobile, third-party), OR
- Your REST API has heavy over-fetching in production (measured), OR
- You're building new client surfaces and want to avoid endpoint proliferation

GraphQL is probably not worth it when:
- You have one or two clients consuming the API
- Your REST endpoints map cleanly to your data model
- Your team has no GraphQL expertise and your backlog is full

**Frame C: Pilot before full migration**
Instead of debating, run a pilot: pick one new feature or client and build it with GraphQL. Run it alongside REST for 2–4 weeks. Let the team experience both sides. This kills theoretical arguments with actual data.

### Recommendation
**Start with Frame A.** Have the team explicitly list the problems they're trying to solve — separate "REST is painful because X" from "GraphQL is cool because Y." If no real problem emerges, you have your answer: don't migrate. If a real problem exists, *then* ask whether GraphQL fixes it better than alternatives (caching strategy, API versioning, request batching, etc.).

If the team still can't agree after that, Frame C (pilot) is cheap insurance. One small GraphQL service alongside REST costs less than a full migration you'll regret.

### Next prompt should include
- What specific problems clients or developers are hitting with the current API (be concrete)
- How many distinct client types you're supporting
- Whether your team has GraphQL experience
- What the "pro" team thinks REST is costing you
- What the "skeptical" team is worried about

Once I see those, I can help you either narrow the decision down to one clear path or design a pilot.