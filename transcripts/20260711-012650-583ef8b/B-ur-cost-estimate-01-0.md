**Trivial — matrix not applied.** Classified this as a factual lookup with arithmetic verification because you're asking for a calculation against published pricing with no unvalidated assumptions in play.

---

## The arithmetic

**Monthly volume:**
- 28 prompts × 5 samples × 2 conditions = 280 API calls per day
- 280 calls/day × 30 days = **8,400 calls/month**

**Tokens per call:**
- Output: 1,000 tokens (given)
- Input: not specified, but test prompts are typically small. I'll estimate **200 input tokens/call** as a reasonable baseline for a test harness. You should substitute your actual average.
- Per-call total: 1,200 tokens

**Monthly tokens:**
- 8,400 calls × 1,200 tokens = **10,080,000 tokens/month**

**Claude 3.5 Haiku pricing** (cheapest Claude model, as of Jan 2025):
- Input: $0.80 per 1M tokens
- Output: $4.00 per 1M tokens

**Cost breakdown:**
- Input cost: 8,400,000 × ($0.80 / 1,000,000) = **$6.72**
- Output cost: 8,400,000 × ($4.00 / 1,000,000) = **$33.60**
- **Total: $40.32/month**

---

## What to verify

- **Input token estimate**: I guessed 200 tokens/prompt. Run one call through your actual prompts and check the usage in the API response. If it's materially different, recalculate: `(input_tokens + 1000) × 8400 × (pricing per token)`.
- **Pricing**: Check [claude.ai/pricing](https://claude.ai/pricing) — these rates were current in Jan 2025 but may have changed.
- **Call volume**: Confirm that 28 × 5 × 2 is the right daily count (no batching, deduplication, or conditional skipping).