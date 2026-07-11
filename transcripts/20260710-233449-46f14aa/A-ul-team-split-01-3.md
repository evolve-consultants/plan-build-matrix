This is worth a structured decision rather than a vote. Here's a practical approach:

**First, clarify what's actually driving each side:**

- GraphQL advocates: Are they frustrated with over-fetching, versioning headaches, or mobile bandwidth? Or just "it's newer"?
- REST defenders: Is it "we're happy with what works" or "I don't want to learn it"?

The real problem matters more than the preference.

**Run a small experiment instead of debating:**

- Pick one non-critical endpoint or service
- Build it in GraphQL with whoever's most enthusiastic
- Use it from an actual client (ideally mobile or bandwidth-constrained)
- Measure: development time, query efficiency, maintenance friction, team velocity
- Compare honestly to the REST equivalent

**Honest trade-offs to evaluate during the trial:**

- GraphQL shines: complex queries, mobile clients, reducing API versions
- GraphQL costs: more upfront learning, caching complexity, debugging can be harder
- REST keeps working fine for: simple CRUD, public APIs, straightforward data fetching

**What often actually matters:**

- Do you have real problems GraphQL solves? (Not hypothetical ones)
- Is your team size/skill level ready for it?
- Will clients actually benefit or just move the N+1 problem around?

**The trap to avoid:** Don't migrate everything at once if you do switch. Parallel REST + GraphQL for a while, retiring REST gradually, is much safer.

What's driving the push on your team—specific pain points or general enthusiasm?