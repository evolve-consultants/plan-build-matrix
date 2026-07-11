**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
Your team is split on whether to migrate from REST to GraphQL. You want a framework for deciding, not just arguments for both sides.

<assumptions>
  <project>You have an existing REST API in production serving real clients. I don't know: the API's age, complexity, client diversity, or current pain points.</project>
  <task>You're looking for a decision-making process, not a mandate. The team disagreement suggests legitimate trade-offs exist on both sides.</task>
  <operator>You have the authority to decide, but you want the team aligned before moving forward. Buy-in matters as much as technical correctness.</operator>
</assumptions>

### What I'm unsure of
- **What problems are driving the GraphQL camp?** (Over-fetching? Unstable client requirements? Multiple versions of the same endpoint? API gateway pressure?)
- **What's driving the skepticism?** (Maintenance cost? Team unfamiliarity? Perceived complexity? Recent sprint velocity concerns?)
- **What's your actual constraint?** (Time to implement? Team size? Client diversity? Rate of schema change?)
- **How much of this is technical vs. team dynamics?** (Is one side more senior/experienced? Does one side feel unheard?)

### The Real Decision

This isn't actually "REST or GraphQL?" — it's **"Do we solve the problem we have with our current API, and is GraphQL the right tool?"**

| | REST stays | GraphQL migration | Hybrid (GraphQL layer on REST) |
|---|---|---|---|
| **Upside** | No migration risk, team familiar, proven, works | Solves over-fetching, unified schema, better mobile experience, alignment with modern stacks | Get GraphQL benefits without rearchitecting backend, lower risk, can migrate incrementally |
| **Downside** | Leaves current pain points unaddressed, may require versioning or gateway complexity as clients diversify | High migration cost, tooling learning curve, caching complexity, team re-training, schema design is hard to get right | Maintains two query layers (operational debt), potential inconsistency, deferred decision |
| **Best when** | Current API is fit-for-purpose, clients are homogeneous or stable, team prefers predictability | Clients are highly diverse, over-fetching is a real problem, you have bandwidth for 2-3 sprint migration + 1-2 sprints of stabilization, team is willing to learn | You have specific GraphQL wins (one problematic client? mobile app?) but aren't ready for full migration, or you want a migration path without full rip-and-replace |

### What should actually happen before a vote

Before choosing, **diagnose what problem you're solving**:

1. **Spend 30 minutes as a team** listing the actual pain points with the current API:
   - What do clients complain about?
   - What's hard to maintain or scale?
   - What decision is GraphQL supposed to fix?

2. **Separate technical from organizational concerns**:
   - Technical: "clients over-fetch 40% of responses" or "versioning is a mess"
   - Organizational: "team wants to use GraphQL on résumés" or "one person championed this and won't let it go"

3. **Set a decision criterion** before the debate. Examples:
   - "We'll do it if it measurably reduces client bandwidth and we can do it in 2 sprints"
   - "We'll stay REST unless three different clients independently request GraphQL"
   - "We'll try the hybrid approach for 6 weeks and then decide"

### Recommendation

**Don't vote. Audit first.**

Set up a 1-hour working session where:
- GraphQL advocates present one real client problem that GraphQL solves better (not theoretical)
- Skeptics present the actual cost/risk estimate (not "it's complex")
- You decide together: "Is that problem worth that cost?"

If they can't do this — if the GraphQL side can't name a specific pain point and the skeptics can't quantify the work — then **the real issue is alignment on priorities, not technology**. A vote won't fix that.

### Next prompt should include
- **The actual pain points** driving the GraphQL conversation (specific examples, not "modern best practice")
- **What the skeptics' main concern is** (cost? complexity? timing? belief it's unnecessary?)
- **Your timeline** (is this blocking other work, or exploratory?)
- Whether you want me to help **design a small proof-of-concept** (safest way to let both sides test their assumptions)