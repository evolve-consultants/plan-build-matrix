**Trivial — matrix not applied.** Classified this as a factual lookup (Claude pricing + basic arithmetic) because the assumptions are already confirmed in the request itself.

---

## The Arithmetic

**Monthly volume:**
- 28 prompts × 5 samples × 2 conditions = 280 API calls per day
- 280 calls/day × 30 days = 8,400 calls per month

**Tokens per call:**
- Output: 1,000 tokens (given)
- Input: assuming ~200 tokens average per prompt (typical for a test suite instruction + context)
- Total per call: ~1,200 tokens

**Total tokens:**
- 8,400 calls × 1,200 tokens = 10,080,000 tokens per month

**Claude pricing (as of my knowledge cutoff, Jan 2025):**
- Cheapest model: Claude 3.5 Haiku
- Input: $0.80 / 1M tokens
- Output: $4.00 / 1M tokens

**Cost breakdown:**
- Input: (28 × 5 × 2 × 30 × 200 tokens) × ($0.80 / 1M) = 1,680,000 × $0.80 / 1M = **$1.34**
- Output: (28 × 5 × 2 × 30 × 1,000 tokens) × ($4.00 / 1M) = 8,400,000 × $4.00 / 1M = **$33.60**

**Total: ~$35/month**

---

**Where to verify:** Check current Haiku pricing at [claude.ai/pricing](https://claude.ai/pricing). If your input tokens/prompt differ materially from 200, recalculate the input line proportionally.