# Claude API Cost Estimation

## Setup
- **Model**: Claude 3.5 Haiku (cheapest option)
- **Pricing**: $0.80/MTok input, $4.00/MTok output
- **Frequency**: Daily for 30 days

## Arithmetic

**Requests per day:**
- 28 prompts × 5 samples × 2 conditions = **280 requests/day**

**Input tokens per day:**
- Assuming ~500 tokens per prompt (typical for test setup)
- 280 requests × 500 tokens = **140,000 input tokens/day**

**Output tokens per day:**
- 280 requests × 1,000 tokens = **280,000 output tokens/day**

**Monthly totals (×30 days):**
- Input: 140,000 × 30 = **4,200,000 tokens**
- Output: 280,000 × 30 = **8,400,000 tokens**

**Monthly cost:**
- Input: (4,200,000 / 1,000,000) × $0.80 = **$3.36**
- Output: (8,400,000 / 1,000,000) × $4.00 = **$33.60**

**Total: ~$37/month**

---

## Key variables to adjust:
- If your actual prompts are shorter/longer, scale the $3.36 proportionally
- If you run tests more/less frequently, scale linearly
- Using Claude 3.5 Sonnet would be ~15× more expensive