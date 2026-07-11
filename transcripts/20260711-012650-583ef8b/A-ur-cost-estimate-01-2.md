# Claude API Cost Estimate for Daily Test Suite

## Parameters
- **Model**: Claude 3.5 Haiku (cheapest option)
- **Pricing**: $0.80/M input tokens, $4.00/M output tokens
- **Daily runs**: 1
- **Working days/month**: 30 (conservative)

## Calculation

**Prompts per day:**
- 28 prompts × 5 samples × 2 conditions = **280 API calls/day**

**Output tokens:**
- 280 calls × 1,000 tokens = **280,000 output tokens/day**

**Input tokens** (rough estimate):
- Assuming ~500 tokens per prompt on average
- 280 calls × 500 = **140,000 input tokens/day**

**Daily cost:**
- Input: (140,000 / 1,000,000) × $0.80 = **$0.112**
- Output: (280,000 / 1,000,000) × $4.00 = **$1.120**
- **Daily total: $1.23**

**Monthly cost (30 days):**
- $1.23 × 30 = **~$37/month**

## Reality check
This assumes modest prompt sizes. If your prompts are longer (~1,000 tokens each), add ~$0.11/day → **~$40/month total**. If they're shorter (~200 tokens), subtract proportionally.