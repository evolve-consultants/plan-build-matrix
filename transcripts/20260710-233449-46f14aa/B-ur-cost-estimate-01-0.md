**Trivial — matrix not applied.** Classified this as a factual lookup (current pricing + straightforward arithmetic) because you've specified all constraints and own verification.

---

## The Calculation

**Claude 3.5 Haiku** (cheapest model as of my last update, Jan 2025):
- Input: $0.80 per million tokens
- Output: $4.00 per million tokens

**Daily test run:**
- 28 prompts × 5 samples × 2 conditions = **280 API calls per day**
- Assume ~200 input tokens per prompt (typical for test harness)
- 280 calls × 200 input tokens = **56,000 input tokens/day**
- 280 calls × 1,000 output tokens = **280,000 output tokens/day**

**Daily cost:**
- Input: (56,000 / 1,000,000) × $0.80 = **$0.0448**
- Output: (280,000 / 1,000,000) × $4.00 = **$1.12**
- Daily total: **$1.1648**

**Monthly cost (30 days):**
- $1.1648 × 30 = **~$35**

---

## Verification Checklist

- [ ] Check current Haiku pricing (I may be out of date)
- [ ] Confirm your input token count (200 is a guess; measure a real prompt)
- [ ] Confirm output token count (you specified 1,000; verify actual usage)
- [ ] Confirm daily frequency (you said daily; if it's weekdays only, multiply by 0.714)

If input tokens are higher, the cost rises proportionally. If you switch to a larger model (Sonnet, Opus), multiply by the cost ratio.