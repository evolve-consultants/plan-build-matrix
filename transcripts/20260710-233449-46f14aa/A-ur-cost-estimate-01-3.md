# Claude API Cost Estimation

## Setup
- **Model**: Claude 3.5 Haiku (cheapest option)
- **Pricing**: $0.80 per 1M input tokens, $4.00 per 1M output tokens

## Daily Calculation

**Requests per day:**
- 28 prompts × 5 samples × 2 conditions = **280 requests/day**

**Output tokens per day:**
- 280 requests × 1,000 tokens = **280,000 output tokens/day**

**Input tokens per day:**
- Assuming ~500 tokens per prompt (you didn't specify, so this is an estimate)
- 280 requests × 500 tokens = **140,000 input tokens/day**

**Daily cost:**
- Input: (140,000 ÷ 1,000,000) × $0.80 = **$0.112**
- Output: (280,000 ÷ 1,000,000) × $4.00 = **$1.12**
- **Daily total: ~$1.23**

## Monthly Cost

**$1.23 × 30 days = $36.90/month**

---

## Notes to adjust:
- **Input token count**: This is my biggest assumption. If your prompts are longer/shorter, multiply them by your actual token count and recalculate
- **Missing variable**: You didn't specify input tokens, so if you know them, plug that in for more accuracy