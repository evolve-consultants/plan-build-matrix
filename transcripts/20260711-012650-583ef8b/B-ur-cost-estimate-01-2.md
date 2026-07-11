**Trivial — matrix not applied.** Classified this as a factual lookup with arithmetic (current pricing + multiplication) because the request is fully specified and I own the calculation verification you're asking for.

---

## Arithmetic

**Monthly volume:**
- 28 prompts × 5 samples × 2 conditions = **280 API calls per day**
- 280 calls/day × 30 days = **8,400 calls per month**

**Tokens per call:**
- Input: assume ~500 tokens per prompt (typical for test setup; adjust if yours are shorter/longer)
- Output: 1,000 tokens (you specified)
- Total per call: **1,500 tokens**

**Total monthly tokens:**
- 8,400 calls × 1,500 tokens = **12,600,000 tokens**

**Pricing (Claude 3.5 Haiku, current):**
- Input: $0.80 per 1M tokens
- Output: $4.00 per 1M tokens

**Cost breakdown:**
- Input cost: (8,400 calls × 500 tokens) ÷ 1M × $0.80 = 4,200,000 ÷ 1M × $0.80 = **$3.36**
- Output cost: (8,400 calls × 1,000 tokens) ÷ 1M × $4.00 = 8,400,000 ÷ 1M × $4.00 = **$33.60**

**Monthly total: ~$37**

---

**Where to sanity-check:**
- Input token count: adjust the ~500 estimate if your actual prompts are known
- Pricing: verify against [Anthropic's current pricing page](https://www.anthropic.com/pricing/claude) (rates change)
- Days per month: I used 30; use 21–22 if you mean business days only