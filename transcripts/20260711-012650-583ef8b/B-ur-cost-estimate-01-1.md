**Trivial — matrix not applied.** Classified this as a factual lookup + arithmetic verification because the numbers are fixed and the calculation is straightforward.

---

## The Arithmetic

**Monthly volume:**
- 28 prompts × 5 samples × 2 conditions = 280 responses per day
- 280 responses/day × 30 days = **8,400 responses/month**
- 8,400 responses × 1,000 output tokens = **8,400,000 output tokens/month**

**Claude 3.5 Haiku pricing** (cheapest Claude model as of my knowledge cutoff):
- Input: $0.80 per million tokens
- Output: $4.00 per million tokens

**Cost calculation:**
- Output cost: (8,400,000 / 1,000,000) × $4.00 = 8.4 × $4.00 = **$33.60/month**
- Input cost: unknown (depends on prompt size; add separately)

**Result: ~$34/month for output alone**, plus input cost.

If your prompts average 500 input tokens each:
- 8,400 responses × 500 tokens = 4,200,000 input tokens/month
- Input cost: (4,200,000 / 1,000,000) × $0.80 = 4.2 × $0.80 = **$3.36/month**

**Total estimate: ~$37.96/month** (output + input).

Check the [Claude pricing page](https://claude.ai/pricing) to confirm current rates, as they may have changed.