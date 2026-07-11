**Operating from: Bottom-Left (Plan + Quality)**

### What I understand you're asking
You've built internal tools at your consultancy (probably to support delivery/ops), and you're considering turning one or more of them into something you sell externally. You want a starting point — not a full roadmap yet, since there's a lot upstream that isn't settled.

<assumptions>
  <project>I don't know what the tool does, its current maturity (script vs. app vs. platform), tech stack, or whether it depends on your specific client contracts/data to function.</project>
  <task>You're exploring turning it into a standalone product (likely licensed/SaaS) rather than just improving it internally. I'm assuming this is still exploratory — you haven't committed capital or a team to it yet.</task>
  <operator>You run a services business, so revenue today comes from billable hours, not product margins. I'm assuming limited dedicated engineering time for productization, and that you'd want to de-risk before investing heavily.</operator>
</assumptions>

### What I'm unsure of
- What problem the tool solves and for whom — internal ops tool, client-facing deliverable accelerator, or something else entirely
- Whether you want to keep the consultancy running as-is alongside this, or eventually pivot the business model
- Whether any external demand signal already exists (have clients asked to buy/license it?)
- IP/ownership clarity — was this built entirely in-house, or does it embed client-derived logic/data that complicates resale

### Here's a rough draft (Option A) — a validation-first starting sequence

1. **Nail the specific problem and buyer.** "Internal tooling" is usually solving a narrow, well-understood pain for *you*. Before building anything new, articulate who else has that exact pain and how they currently deal with it without your tool.
2. **Validate demand before building further.** Talk to 5-10 people outside your company who fit the buyer profile (former clients, peers, prospects). Gauge if they'd pay, not just if they'd use it for free.
3. **Scope the productization gap.** Internal tools are usually held together by tribal knowledge, hardcoded assumptions, and no onboarding. List what's missing for a stranger to use it unsupervised: multi-tenancy, auth, docs, support, billing.
4. **Decide packaging and pricing early**, even roughly — it changes what "productized" needs to mean (self-serve SaaS vs. white-glove licensed tool have very different bars).
5. **Pick a go-to-market motion that uses what you already have** — your existing client relationships and reputation are usually the fastest distribution channel, more so than cold market entry.
6. **Decide the structural question last, not first**: separate entity/product line vs. a service-business add-on. This is a lagging decision, not a leading one — resist solving it too early.

### Alternatives I considered
- **B — Start with the IP/ownership question.** If there's any chance the tool embeds client-specific logic, data, or was built under contracts with IP assignment clauses, that could block productization entirely regardless of demand. Worth leading with this if you're not 100% sure you own it outright.
- **C — Skip validation, go straight to productization roadmap.** Makes sense if you already have concrete proof (e.g., multiple clients have explicitly asked to license or buy it). If that's your situation, we can jump straight to scoping/pricing/GTM instead of demand validation.

### Next prompt should include
- What the tool actually does, at a high level, and who it's for
- Whether any client has already asked for or expressed interest in this as a product
- Whether you want to keep consulting running unchanged for now, or whether this is a long-term pivot
- Whether B (IP check) or C (skip to roadmap) fits your situation better than the validation-first draft above