# Claude API Cost Estimation for Daily Test Suite

## Parameters
- **Model**: Claude 3.5 Haiku (cheapest option)
- **Frequency**: Daily
- **Days per month**: 30

## Pricing (Current Claude 3.5 Haiku rates)
- Input: $0.80 per 1M tokens
- Output: $4.00 per 1M tokens

## Arithmetic

**Per API call:**
- Input tokens: ~500 (rough estimate for typical prompt)
- Output tokens: 1,000 (given)
- Total per call: 1,500 tokens

**Daily volume:**
- 28 prompts × 5 samples × 2 conditions = **280 API calls/day**
- Tokens/day: 280 calls × 1,500 tokens = **420,000 tokens/day**

**Monthly volume (30 days):**
- Total tokens: 420,000 × 30 = **12,600,000 tokens/month**
- Input proportion: ~33% = 4,200,000 tokens
- Output proportion: ~67% = 8,400,000 tokens

**Monthly cost:**
- Input: (4,200,000 / 1,000,000) × $0.80 = **$3.36**
- Output: (8,400,000 / 1,000,000) × $4.00 = **$33.60**
- **Total: ~$37/month**

---

**Check your assumptions**: If your actual prompt size differs significantly from 500 tokens, adjust the input token count proportionally.