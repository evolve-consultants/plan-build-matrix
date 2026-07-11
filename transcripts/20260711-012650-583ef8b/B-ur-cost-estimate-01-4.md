**Trivial — matrix not applied.** Classified this as a factual lookup + arithmetic verification because there are no unvalidated assumptions about intent, context, or downstream decisions in play.

---

## Monthly API Cost Calculation

**Setup:**
- Cheapest Claude model: Claude 3.5 Haiku
- Input cost: $0.80 per 1M tokens
- Output cost: $2.40 per 1M tokens

**Daily run volume:**
- 28 prompts × 5 samples × 2 conditions = **280 API calls per day**
- ~1000 output tokens per response
- Input tokens: assume ~500 per prompt (typical for test harness setup)

**Per-call cost:**
- Input: 500 tokens × ($0.80 / 1M) = $0.0004
- Output: 1000 tokens × ($2.40 / 1M) = $0.0024
- **Per call: $0.0028**

**Daily cost:**
- 280 calls × $0.0028 = **$0.784 per day**

**Monthly cost (30 days):**
- $0.784 × 30 = **~$23.50/month**

---

**Arithmetic check:**
- 280 calls/day × 30 days = 8,400 calls/month
- 8,400 × 500 input tokens = 4.2M input tokens/month → $3.36
- 8,400 × 1000 output tokens = 8.4M output tokens/month → $20.16
- **Total: $23.52** ✓