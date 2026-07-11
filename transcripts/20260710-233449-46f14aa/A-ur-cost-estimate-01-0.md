# Claude API Cost Estimate

## Setup
- **Model**: Claude 3.5 Haiku (cheapest option)
- **Pricing**: $0.80/M input tokens, $4.00/M output tokens

## Daily Test Suite

**Prompts per day:**
- 28 prompts × 5 samples × 2 conditions = **280 API calls/day**

**Tokens per day:**
- Input: Assuming ~500 tokens per prompt (typical for test prompts)
  - 280 calls × 500 tokens = **140,000 input tokens/day**
- Output: Given
  - 280 calls × 1,000 tokens = **280,000 output tokens/day**

**Daily cost:**
- Input: (140,000 / 1,000,000) × $0.80 = **$0.112**
- Output: (280,000 / 1,000,000) × $4.00 = **$1.120**
- **Daily total: $1.232**

## Monthly Cost

$1.232/day × 30 days = **~$37/month**

---

## Sanity check
If input tokens are actually lighter (~250/prompt), you'd be closer to **$30/month**. If heavier (~750/prompt), closer to **$45/month**.