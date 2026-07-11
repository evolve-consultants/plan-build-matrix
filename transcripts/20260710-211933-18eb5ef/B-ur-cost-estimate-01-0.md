**Trivial — matrix not applied.** Classified this as a factual lookup with straightforward arithmetic because the question is self-contained, the variables are specified, and I'm doing the calculation once, not building something iterative or ambiguous.

---

## The Arithmetic

**Monthly volume:**
- 28 prompts × 5 samples × 2 conditions = **280 API calls per day**
- 280 calls/day × 30 days = **8,400 calls per month**

**Tokens per call:**
- Output: 1,000 tokens (specified)
- Input: varies by prompt, but let's estimate conservatively. A typical test prompt is 200–500 tokens. I'll use **400 tokens input** as a middle ground.
- **Total per call: ~1,400 tokens**

**Monthly token volume:**
- 8,400 calls × 1,400 tokens = **11,760,000 tokens per month**

**Claude 3.5 Haiku pricing** (cheapest model as of Jan 2025):
- Input: $0.80 per 1M tokens
- Output: $4.00 per 1M tokens

**Cost breakdown:**
- Input: (28 × 5 × 2 × 30 × 400 tokens) × ($0.80 / 1M) = 3,360,000 × $0.80 / 1M = **$2.69**
- Output: (28 × 5 × 2 × 30 × 1,000 tokens) × ($4.00 / 1M) = 8,400,000 × $4.00 / 1M = **$33.60**

**Total: ~$36.29 per month**

---

## Check Your Inputs

If your actual input prompt length differs materially from 400 tokens, adjust the input line. If you're using a different model (Claude 3.5 Sonnet is ~3× the cost), multiply the total by that factor. If daily cadence varies, scale the 30-day multiplier.