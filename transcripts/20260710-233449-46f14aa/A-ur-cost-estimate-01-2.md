# Claude API Cost Estimate

## Setup
- **Model**: Claude 3.5 Haiku (cheapest option)
- **Pricing**: $0.80/MTok input, $4.00/MTok output
- **Frequency**: Daily

## Arithmetic

**Per test run:**
- Prompts: 28
- Samples per prompt: 5
- Conditions: 2
- Total API calls: 28 × 5 × 2 = **280 calls**
- Output tokens per call: 1,000
- Total output tokens per run: 280 × 1,000 = **280,000 tokens**

**Per month (30 days):**
- Total output tokens: 280,000 × 30 = **8,400,000 tokens**
- Output cost: 8,400,000 ÷ 1,000,000 × $4.00 = **$33.60**

**Input tokens** (typically smaller):
- Assuming ~500 input tokens per call on average
- 280 calls × 500 = 140,000 tokens/day
- Monthly: 140,000 × 30 = 4,200,000 tokens
- Input cost: 4,200,000 ÷ 1,000,000 × $0.80 = **$3.36**

## **Total Monthly Cost: ~$37**

This scales proportionally—double your samples and you're at ~$74/month. The output tokens dominate the cost here.