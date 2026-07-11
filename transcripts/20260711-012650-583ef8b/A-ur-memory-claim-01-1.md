# LLM API Rate Limits: Structure & Implementation

## General Knowledge (Standard Across Most Providers)

### Tier Structure
Most LLM providers use **consumption-based tiers**:
- **Free/Trial**: Limited requests (often 3-5 per minute, strict daily caps)
- **Pay-as-you-go**: Higher limits, scales with spending
- **Enterprise**: Custom negotiated limits

### Primary Rate Limit Metric: Tokens Per Minute (TPM)
- Limits measure **input + output tokens**, not requests
- Example: "100K TPM" = 100,000 tokens across all requests in 60 seconds
- More granular than request-per-minute because token usage varies wildly

### HTTP Headers (Standard Pattern)
Providers typically return these headers:
```
x-ratelimit-limit-requests: 100          # max requests/minute
x-ratelimit-limit-tokens: 100000         # max tokens/minute
x-ratelimit-remaining-requests: 87
x-ratelimit-remaining-tokens: 92150
x-ratelimit-reset-requests: 2024-01-15T10:35:00Z
x-ratelimit-reset-tokens: 2024-01-15T10:35:00Z
```

### Retry Logic (Standard Approach)
- **429 status code** = rate limit hit
- **Exponential backoff** recommended: wait 2^n seconds, with jitter
- Check `retry-after` header if present (in seconds)
- Wait until `x-ratelimit-reset-*` timestamp before retrying

## Provider-Specific Details (VERIFY FOR YOUR USE CASE)

| Aspect | Why It Varies | What to Check |
|--------|--------------|---------------|
| **Limit metrics** | Some use requests/min instead of TPM; others combine both | Provider's rate limit documentation |
| **Soft vs. hard limits** | Some allow brief bursts; others strictly enforce | Rate limit policies page |
| **Per-request vs. global** | Enterprise may have per-API-key and account-level limits | Billing/limits dashboard |
| **Batch endpoints** | Often have separate, higher limits | Batch API documentation |
| **Model-specific limits** | Larger models may have lower TPM | Model-specific pages |
| **Header names** | Some use different prefixes (`ratelimit-` vs `x-ratelimit-`) | API reference docs |
| **Reset timing** | Token resets: rolling window vs. fixed minute boundaries | Clarify before designing retry logic |
| **Quota vs. rate limit** | Some distinguish daily quotas from per-minute rate limits | Account settings & pricing page |

## Practical Implementation Checklist

**Before deploying:**
- [ ] Get exact TPM/RPM for your tier from dashboard or API
- [ ] Test rate limit headers with a small request to see exact format
- [ ] Confirm reset timing (does `x-ratelimit-reset-tokens` use rolling or fixed windows?)
- [ ] Check if batch/async endpoints have different limits
- [ ] Verify whether limits are per-key, per-project, or per-account
- [ ] Read provider's guidance on concurrent requests
- [ ] Test your retry logic against actual 429 responses in sandbox

## Red Flags (Clarify Immediately)

- Vague limits like "reasonable use"
- No rate limit headers in responses
- Undocumented difference between stated and actual limits
- Different limits for different regions/deployments

Would you like provider-specific guidance for a particular service (OpenAI, Anthropic, etc.)?