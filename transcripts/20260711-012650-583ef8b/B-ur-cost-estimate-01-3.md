**Trivial — matrix not applied.** Classified this as a factual lookup with straightforward arithmetic because no unvalidated assumptions are in play and the answer is directly checkable against published pricing.

---

## The Arithmetic

**Daily volume:**
- 28 prompts × 5 samples × 2 conditions = 280 API calls per day
- 280 calls × ~1000 output tokens = 280,000 output tokens/day

**Monthly volume (30 days):**
- 280 calls × 30 = 8,400 API calls
- 280,000 tokens × 30 = 8,400,000 output tokens/month

**Pricing (Claude 3.5 Haiku, cheapest model as of Jan 2025):**
- Input: $0.80 per 1M tokens
- Output: $4.00 per 1M tokens

**Cost calculation:**
- Output cost: 8,400,000 ÷ 1,000,000 × $4.00 = **$33.60/month**
- Input cost: depends on prompt size (you didn't specify). Assume modest prompts (~500 tokens each):
  - 8,400 calls × 500 tokens = 4,200,000 input tokens
  - 4,200,000 ÷ 1,000,000 × $0.80 = **$3.36/month**

**Total: ~$37/month** (output-dominated; input cost varies with prompt length)

---

**To check this yourself:** Verify [Anthropic's current pricing](https://www.anthropic.com/pricing/claude) for Haiku, then multiply: (daily_calls × output_tokens × 30) ÷ 1,000,000 × output_rate_per_M.