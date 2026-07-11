# Claude API Cost Estimation

## Parameters
- **Model**: Claude 3.5 Haiku (cheapest option)
- **Pricing**: $0.80/M input tokens, $4.00/M output tokens
- **Frequency**: Daily test suite
- **Days/month**: 30

## Calculation

**Per test run:**
- Prompts: 28
- Samples per prompt: 5
- Conditions: 2
- Total API calls: 28 × 5 × 2 = **280 calls**
- Output tokens per call: 1,000
- Total output tokens: 280 × 1,000 = **280,000 tokens**

**Input tokens (estimated):**
- Assuming ~500 input tokens per prompt on average
- 28 prompts × 500 tokens = 14,000 tokens per run
- With 5 samples × 2 conditions: 14,000 × (5 × 2) = **140,000 input tokens** per run

**Daily cost:**
- Input: (140,000 / 1,000,000) × $0.80 = **$0.112**
- Output: (280,000 / 1,000,000) × $4.00 = **$1.120**
- Daily total: **$1.232**

**Monthly cost:**
- $1.232 × 30 days = **~$37/month**

---

## Sensitivity
If your actual input tokens differ, adjust the daily total proportionally. The output cost ($1.12/day) is fixed by your parameters; input is the variable.