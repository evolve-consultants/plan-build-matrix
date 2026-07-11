**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You've built internal tools that work well for your consultancy and you're exploring whether they could become a standalone product. You're looking for a framework or first steps to evaluate and begin that transition.

<assumptions>
  <project>You have working software that solves a real problem you experience daily. You likely have some domain expertise in the problem space.</project>
  <task>You want to understand whether a product business makes sense here and what the path forward looks like, not necessarily to commit to building it yet.</task>
  <operator>You're running a consultancy (so you have limited time and existing revenue), and you're asking this now which suggests you're past the "is this crazy?" stage but not yet committed.</operator>
</assumptions>

### What I'm unsure of
- **Market positioning**: Is this a tool for consultants like you, or a broader category? (Huge difference in TAM and go-to-market)
- **Current maturity**: Are we talking "scripts that work for us" or "polished, documented, somewhat maintainable"?
- **Your goal**: Do you want to build a new company, create a revenue stream alongside consulting, or explore selling to your competitors?
- **Constraints**: How much time could you realistically invest? Are co-founders involved?

### The four decision gates (in order)

| Gate | Question | Signals to move forward | Red flags |
|---|---|---|---|
| **1. Customer fit** | Does anyone else actually want this, or just you? | Other consultants have asked for it / you've seen the problem elsewhere | Only you have this problem / your clients don't care |
| **2. Extractability** | Can you separate it from your consultancy's IP and operations? | It solves a generic problem / minimal client-specific logic | Deeply baked into your workflows / contains client data |
| **3. Defensibility** | Why can't someone else build this in 6 months? | Unique data / network effects / deep domain expertise / significant complexity | It's straightforward to replicate |
| **4. Economics** | Is the unit economics viable? | High gross margin potential / customers will pay / low support burden | Low willingness to pay / customization-heavy / high support cost |

### Three parallel paths forward

**Path A: Validate first, build product second** (Recommended if you're genuinely unsure)
- Talk to 10–15 non-customers who have the problem. Not "would you buy this?" but "how do you solve this now and what's broken?"
- Offer to let 2–3 use your tool for free in exchange for brutal feedback.
- Decide: does the problem matter enough that they'd pay? Do you hear the same problems repeatedly?
- **Time**: 4–6 weeks. **Output**: clear signal on whether to proceed.

**Path B: Package and test with warm leads** (Recommended if you have existing relationships)
- Document the tool enough that someone outside your team could use it (not polished, just usable).
- Offer it to 3–5 friendly competitors or adjacent consultancies at a steep discount ($X/month).
- Watch: Are they actually using it? Do they ask for features? Do they refer others?
- **Time**: 8–12 weeks. **Output**: early revenue signal + product feedback.

**Path C: Build in parallel while consulting** (Recommended if you have a co-founder or team member to own it)
- One person goes half-time on productization while the consultancy continues.
- Goal: ship something minimal but self-serve in 3 months.
- **Time**: ongoing. **Output**: real usage data faster, but requires bandwidth.

### Red flags to reconsider
- You're the only person who's asked for this → validation is weak
- Your tool is 60%+ integrations or glue code → extract and test that assumption first
- Your clients would be uncomfortable with you selling to competitors → IP or NDA issues to resolve
- You'd need to be hands-on support for each customer → not a product play

### Next prompt should include
- Which of the four gates concerns you most?
- Is this exploratory (Path A) or are you leaning into one of the others?
- What's the tool do (one sentence) and who'd use it?
- How much time could you or a co-founder realistically allocate?