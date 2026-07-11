# Claude API Cost Estimate for Test Suite

## Setup
- **Model**: Claude 3.5 Haiku (cheapest option)
- **Pricing**: $0.80/M input tokens, $4.00/M output tokens

## Daily Calculation

**Prompts per day:**
- 28 prompts × 5 samples × 2 conditions = **280 API calls/day**

**Output tokens per day:**
- 280 calls × 1,000 tokens = **280,000 output tokens/day**

**Input tokens per day:**
- You didn't specify input size. I'll assume **500 tokens/prompt** (typical for test cases)
- 280 calls × 500 tokens = **140,000 input tokens/day**

## Monthly Calculation (30 days)

**Output cost:**
- 280,000 tokens/day × 30 days = 8,400,000 tokens
- 8,400,000 × ($4.00/M) = **$33.60**

**Input cost:**
- 140,000 tokens/day × 30 days = 4,200,000 tokens
- 4,200,000 × ($0.80/M) = **$3.36**

## **Total: ~$36.96/month**

---

**To adjust:** If your actual input prompt size differs, multiply (tokens/prompt) × 280 × 30 × $0.80/M.