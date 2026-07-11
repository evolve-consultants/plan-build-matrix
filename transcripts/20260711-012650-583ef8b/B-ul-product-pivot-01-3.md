**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You've built internal tools that work well for your consultancy, and you're considering whether (and how) to productize them — turn them into something you could sell or license to other consultancies or similar buyers. You need a starting framework.

<assumptions>
  <project>You have working software that solves real problems for your business. It's not theoretical.</project>
  <task>You want to understand the sequencing: what to validate first, what can wait, how to think about the transition.</task>
  <operator>You're running a consultancy (so you understand customer problems and service delivery), but you may not have experience with product development, go-to-market, or the different skill sets involved.</operator>
</assumptions>

### What I'm unsure of
- **What type of tool** (workflow automation, analytics, client-facing portal, back-office system, etc.) — this changes the complexity of productization significantly
- **Current state**: Is it a single monolithic app or modular components? How coupled is it to your internal processes?
- **Your constraint**: Are you thinking of bootstrapping this alongside the consultancy, or would you shift focus? This changes the pace.
- **Your buyer**: Same consultancies like yours, a wider market, or specific verticals?
- **Your goal**: Revenue stream, exit, new business line, or something else?

### Three approaches, ordered by validation-first risk

| | **Risk** | **Timeline** | **Best when** |
|---|---|---|---|
| **A: Talk-first** | Falsest validation (people say yes, don't buy) | 4-8 weeks | You're uncertain whether external demand exists; you want to stay in execution mode during research |
| **B: MVP-first** | Longest runway; highest sunk cost if you're wrong | 3-4 months | You're confident about demand and know exactly what to strip down; you want to prove technical viability fast |
| **C: Hybrid** | Middle ground; highest effort up front | 8-12 weeks | You want both customer validation *and* early technical learning without committing to a full MVP |

### **Recommendation: Approach C (Hybrid)**

Start by doing *talk* work (4-6 weeks) in parallel with *technical* work (2-3 weeks). Here's why:

- **Validation first**: Before you architect a product, confirm that other consultancies actually want this and understand what they'd pay for it. (Your internal use case doesn't guarantee external product-market fit.)
- **Technical option-finding**: Spend 2-3 weeks with a technical co-founder or architect exploring: Can this be decoupled from your internal systems? What's the minimal reusable core? Are there regulatory/compliance gotchas for external users?
- **Colliding them**: By week 6-8, you'll have real customer conversations *and* technical clarity. This collision point tells you whether to double down, pivot, or kill it.

### The immediate next steps (in order)

1. **Identify 10-15 peer consultancies** (direct competitors or adjacent verticals) who'd use this tool. Make a list with contact names.
2. **Define the one problem** your tool solves in customer language (not your language). Write it in one sentence.
3. **Schedule 5 exploratory calls** this week with those peers. Script: "We built X for ourselves. We're exploring whether other consultancies would want it. Can I ask you a few questions about how you handle Y?" Listen for: pain, frequency, current workaround cost.
4. **Parallel: Set up a 2-hour technical spike** with whoever understands the codebase best. Map: what's core logic (must ship), what's internal scaffolding (can strip), what's risky to expose (compliance, data, scaling).

After those calls and that spike, you'll have real data to decide whether to proceed and in what direction.

### Next prompt should include
- What type of tool this is (so I can anticipate productization-specific gotchas)
- Whether you have a technical co-founder or do you need to think through the build solo
- Whether you're trying to keep this revenue-generative in year 1 or whether it's a longer runway play
- Any early signals you've seen (customers asking, colleagues suggesting you sell it, etc.)