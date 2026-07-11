This is worth resolving because the answer genuinely depends on your specifics, and both sides probably have valid points.

**Ask these questions first:**

- **What problems are people actually trying to solve?** Over-fetching? Under-fetching? Frontend complexity? If it's vague ("GraphQL is modern"), that's a red flag. If it's concrete ("mobile clients waste 60% bandwidth"), that matters.

- **What's your current pain?** A stable REST API serving stable clients is low-priority to change. An API with 20 client-specific endpoints or constant versioning headaches is different.

- **What's the real cost?** Not just migration—ongoing maintenance, team learning curve, tooling. GraphQL isn't free operationally.

**Red flags for "do it":**
- Solving problems you don't actually have
- Assuming it'll solve architectural issues it won't
- Team excitement without concrete use cases

**Good reasons to consider it:**
- Multiple clients with genuinely different data needs
- Chronic over/under-fetching problems
- A frontend team that'd measurably benefit
- You have bandwidth to do it properly (not "quick migration")

**A middle path:** Run a 2-week spike. Have skeptics and advocates design the same 2-3 real endpoints in both. Actually compare—performance, code quality, client code. The honest comparison usually settles this better than arguments.

What specific problems is the "move to GraphQL" camp citing?