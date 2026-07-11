**Trivial — matrix not applied.** Classified this as a factual lookup with straightforward arithmetic because the request is fully specified and the answer doesn't depend on unvalidated assumptions about your environment or constraints.

---

## The Arithmetic

**Daily volume:**
- 28 prompts × 5 samples × 2 conditions = **280 API calls per day**
- 280 calls × 1,000 output tokens = **280,000 output tokens per day**

(Assuming input tokens are negligible or already accounted for in "1000 output tokens per response." If you meant 1000 *total* tokens, let me know and I'll recalculate.)

**Monthly volume (30 days):**
- 280,000 tokens/day × 30 days = **8,400,000 output tokens per month**

**Cost:**
Claude 3.5 Haiku is the cheapest model at **$0.80 per 1M output tokens** (as of my last update, January 2025).

- 8,400,000 tokens × ($0.80 / 1,000,000) = **$6.72 per month**

---

**Verification points:**
- Confirm Haiku pricing hasn't changed (check [claude.ai/pricing](https://claude.ai/pricing))
- Confirm "1000 output tokens" is output-only, not total tokens
- If input tokens are substantial, multiply by your average input size and add $0.10 per 1M input tokens