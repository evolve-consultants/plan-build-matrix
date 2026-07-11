# Claude API Cost Estimate

## Parameters
- **Model**: Claude 3.5 Haiku (cheapest option)
- **Pricing**: $0.80/MTok input, $4.00/MTok output
- **Frequency**: Daily test suite
- **Days/month**: 30

## Arithmetic

**Requests per day:**
- 28 prompts × 5 samples × 2 conditions = **280 requests/day**

**Output tokens per day:**
- 280 requests × 1,000 tokens = **280,000 tokens/day**
- 280,000 × 30 days = **8,400,000 tokens/month**

**Output cost:**
- 8,400,000 ÷ 1,000,000 = 8.4 MTok
- 8.4 MTok × $4.00 = **$33.60/month**

**Input tokens per day:**
(Assuming typical prompt size ~500 tokens, adjust if yours differ)
- 280 requests × 500 tokens = **140,000 tokens/day**
- 140,000 × 30 days = **4,200,000 tokens/month**

**Input cost:**
- 4,200,000 ÷ 1,000,000 = 4.2 MTok
- 4.2 MTok × $0.80 = **$3.36/month**

## **Total: ~$37/month**

**Note:** Input cost is negligible here; output dominates. If your prompts are longer/shorter than 500 tokens, scale the input section proportionally.