**Trivial — matrix not applied.** Classified this as a factual lookup with straightforward arithmetic because the request is self-contained, the pricing is fixed, and the calculation has no downstream dependencies that would benefit from exploring assumptions.

---

## The Arithmetic

**Setup:**
- 28 prompts × 5 samples × 2 conditions = **280 API calls per day**
- 280 calls/day × 30 days = **8,400 calls per month**
- ~1,000 output tokens per response

**Pricing (Claude 3.5 Haiku — cheapest model as of Jan 2025):**
- Input: $0.80 per 1M tokens
- Output: $4.00 per 1M tokens

**Output cost:**
- 8,400 calls × 1,000 tokens = 8,400,000 output tokens/month
- 8,400,000 ÷ 1,000,000 = 8.4M tokens
- 8.4M × $4.00 = **$33.60/month**

**Input cost:**
- You didn't specify input token count. If each prompt averages ~500 input tokens:
  - 8,400 calls × 500 tokens = 4,200,000 input tokens/month
  - 4.2M × $0.80 = **$3.36/month**

**Total (with 500-token input assumption): ~$36.96/month**

If your prompts are shorter or longer, scale the input linearly. The output cost ($33.60) is solid given your stated 1000 tokens/response.