# Claude API Cost Calculation

## Setup
- **Model**: Claude 3.5 Haiku (cheapest option)
- **Pricing**: $0.80/MTok input, $4.00/MTok output
- **Run frequency**: Daily for ~30 days

## Daily Calculation

**Prompts per run:**
- 28 prompts × 5 samples × 2 conditions = **280 API calls per day**

**Output tokens per day:**
- 280 calls × 1,000 tokens = **280,000 output tokens/day**

**Input tokens per day:**
- Assuming ~500 tokens average per prompt: 280 × 500 = **140,000 input tokens/day**

## Monthly Calculation (30 days)

**Input:**
- 140,000 tokens/day × 30 days = 4,200,000 tokens
- 4.2M tokens × $0.80/MTok = **$3.36**

**Output:**
- 280,000 tokens/day × 30 days = 8,400,000 tokens
- 8.4M tokens × $4.00/MTok = **$33.60**

## **Total: ~$37/month**

---

**Notes**: 
- This assumes the 500 token/prompt input estimate—adjust upward if your actual prompts are longer
- Haiku is ~3x cheaper than Sonnet; using Sonnet would be ~$111/month
- Adding request overhead (batching, retries) might add 10-20%