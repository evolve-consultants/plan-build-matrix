**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You've built internal tools that work well for your consultancy, and you're exploring whether productizing them is viable — and if so, what the first concrete steps are.

<assumptions>
  <project>You have working software that solves a real problem (for you, at minimum). It probably isn't production-hardened or designed for external users yet.</project>
  <task>You want to understand the decision framework and immediate next steps, not a full go-to-market plan.</task>
  <operator>You're running the consultancy (or have input on major decisions) and have some technical credibility but may not have shipped a product before.</operator>
</assumptions>

### What I'm unsure of
- **Problem fit**: Is the tool solving a problem you see in your *clients*, or just something you built to run your own business better?
- **Market size intuition**: Do you have a sense of whether other firms like yours would pay for this, or is that part of what you're trying to validate?
- **Current state**: How much rewrite would the tool need to be safe for external use? (This changes the effort estimate dramatically.)
- **Appetite**: Are you exploring this as a potential second revenue stream, or would it eventually replace the consultancy?

### Three entry points

| | Upside | Downside | Best when |
|---|---|---|---|
| **A: Customer discovery first** | You validate demand before building anything. You'll talk to 10–15 people who *look* like customers and learn what actually matters to them. Cheap, fast, kills bad ideas early. | You might discover no one cares. Emotionally harder than coding. Takes 2–4 weeks. | You're unsure whether the problem is real for anyone but you. This is the safest first step. |
| **B: Productize what you have** | You get something shippable quickly. You can charge real money and learn from actual users. Feels like progress. | You might build the wrong thing, waste weeks, or find out no one wants it in its current form. Risk of sunk-cost thinking. | You're very confident the tool solves a problem people will pay for, and you want to start generating signal (revenue, user feedback) now. |
| **C: Hybrid — light discovery + minimal MVP** | You do 3–5 customer conversations to sharpen your hypothesis, then build a deliberately narrow first version. Best of both. | Slightly slower than pure discovery, but only because you're building. | You have medium confidence and want to move faster than pure customer discovery, but aren't ready to bet on your current version. |

### Recommendation
**Start with Option A: 10–15 customer discovery conversations.**

Why: The difference between "we use this internally and it's great" and "paying external customers will use this" is enormous. You'll learn more in three weeks of talking to prospects than in three months of building. And if the market signal is weak, you've lost only time, not 6 months of engineering effort.

The specific next step: identify 10–15 people who match your ideal customer profile (similar businesses, similar problems), and ask them to coffee/Zoom for 30 minutes. The conversation is simple: "We built a tool to solve [problem]. Does this sound like something you face? How do you handle it today?" Listen for pain, willingness to change, and anything that surprises you.

### Next prompt should include
- Who you think your customer is (role, company size, industry)
- What problem the tool solves
- Whether you've already heard customers mention this problem, or you're inferring it
- How much time you're willing to invest before deciding to build/pivot/kill the idea