**Trivial — matrix not applied.** Classified this as a factual lookup with arithmetic you can verify, so no unvalidated assumptions are in play.

---

## The Calculation

**Monthly volume:**
- 28 prompts × 5 samples × 2 conditions = 280 API calls per day
- 280 calls/day × 30 days = **8,400 calls per month**

**Tokens per call:**
- 1,000 output tokens per response (given)
- Input tokens vary by prompt; assume ~500 tokens average per prompt (typical for test prompts)
- Per call: ~500 input + ~1,000 output = **1,500 tokens per call**

**Total tokens per month:**
- 8,400 calls × 1,500 tokens/call = **12,600,000 tokens**

**Pricing (Claude 3.5 Haiku, current rates):**
- Input: $0.80 per 1M tokens
- Output: $4.00 per 1M tokens
- Weighted average: (500 input + 1,000 output) / 1,500 = ~$2.93 per 1,000 tokens

**Monthly cost:**
- 12,600,000 tokens × ($2.93 / 1,000,000) = **~$37/month**

---

## Breakdown by component
| Component | Calculation | Result |
|-----------|-------------|--------|
| Daily calls | 28 × 5 × 2 | 280 |
| Monthly calls | 280 × 30 | 8,400 |
| Input tokens/call | (assumed) | 500 |
| Output tokens/call | (given) | 1,000 |
| Total tokens/month | 8,400 × 1,500 | 12.6M |
| Cost/1M tokens | (0.8×500 + 4×1,000)/1,500 | $2,933 |
| **Monthly total** | **12.6M × $2.93/M** | **$37** |

*(Input token count is an assumption — if your prompts are shorter or longer, adjust the 500 figure and recalculate.)*