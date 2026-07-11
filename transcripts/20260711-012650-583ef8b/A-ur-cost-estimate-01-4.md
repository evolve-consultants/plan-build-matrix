# Monthly API Cost Estimate for Test Suite

## Setup
- **Model**: Claude 3.5 Haiku (cheapest at $0.80/M input, $4.00/M output tokens)
- **Daily runs**: 1
- **Days per month**: 30

## Arithmetic

**Prompts per day:**
- 28 prompts × 5 samples × 2 conditions = **280 prompts/day**

**Output tokens per day:**
- 280 prompts × 1,000 tokens = **280,000 output tokens/day**

**Input tokens per day:**
Assuming ~500 tokens per prompt (you'd need to measure your actual prompts):
- 280 prompts × 500 tokens = **140,000 input tokens/day**

**Monthly tokens:**
- Input: 140,000 × 30 = 4,200,000 tokens
- Output: 280,000 × 30 = 8,400,000 tokens

**Monthly cost:**
- Input: 4,200,000 × ($0.80/1,000,000) = **$3.36**
- Output: 8,400,000 × ($4.00/1,000,000) = **$33.60**
- **Total: ~$37/month**

## Sensitivity Notes
- This scales linearly with input token count (heavily dependent on your actual prompt size)
- Output cost dominates at 90% of total
- Verify your actual prompt size by checking API logs

**Check your math:** What's your typical prompt size in tokens?