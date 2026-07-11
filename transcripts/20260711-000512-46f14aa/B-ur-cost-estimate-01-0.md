**Operating from: Upper-Right (Build + Verify)**

### What I understand you're asking
A back-of-envelope monthly cost for running this suite daily, using current cheapest-tier Claude pricing, with the arithmetic exposed so you can audit or swap in your own numbers.

<assumptions>
<project>No codebase involved — this is a standalone pricing estimate, not tied to a specific integration.</project>
<task>You want a defensible ballpark, not a precise invoice — arithmetic shown so wrong inputs are easy to swap.</task>
<operator>You'll plug in real input-token counts and current pricing yourself; I shouldn't guess too hard on either.</operator>
</assumptions>

### The artifact

**Step 1 — requests per day**
```
28 prompts × 5 samples × 2 conditions = 280 API calls/day
```

**Step 2 — output tokens**
```
280 calls/day × 1,000 output tokens = 280,000 output tokens/day
280,000 × 30 days  = 8,400,000 output tokens/month  (8.4M)
```
*(using 30 days — swap for 30.44 if you want a true average month)*

**Step 3 — output cost**
```
Cheapest current Claude tier: Claude 3 Haiku
  Output: $1.25 / 1M tokens   <!-- assumed: verify against current pricing page -->
  Input:  $0.25 / 1M tokens   <!-- assumed: verify against current pricing page -->

8.4M output tokens × $1.25/1M = $10.50
```

**Step 4 — input cost (the actual gap in your numbers)**
You didn't give a prompt length, so I can't compute this for real — I'm placeholding at 500 input tokens/prompt:
```
280 calls/day × 500 input tokens  = 140,000 input tokens/day
140,000 × 30 days                 = 4,200,000 input tokens/month (4.2M)
4.2M × $0.25/1M                   = $1.05
```

**Total estimate**
```
$10.50 (output) + $1.05 (input, guessed length) ≈ $11.55/month
```

### What I'm confident about
- The request-count arithmetic (280/day, 8,400/month) — pure multiplication from your numbers, no assumptions.
- Output token volume (8.4M/month) — follows directly from your ~1000 tokens/response figure.

### What I'd double-check
- **Current pricing**: I'm using Claude 3 Haiku at $0.25/$1.25 per M tokens from memory — if pricing has changed or Haiku's been superseded by a cheaper tier, the whole output-cost number scales linearly. This is the single biggest lever on the final total.
- **Input tokens**: I used a placeholder of 500 tokens/prompt. If your actual prompts are longer (e.g., few-shot examples, long context), input cost could dominate rather than being a rounding error — recompute Step 4 with your real number.
- **Days/month**: used 30 flat; using 30.44 changes the total by ~1.5%, immaterial here.