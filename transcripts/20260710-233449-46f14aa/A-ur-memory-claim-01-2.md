# LLM API Rate Limiting: General Patterns & Verification Points

## General Knowledge (Common Industry Patterns)

### Tier-Based Structures
Most providers use pricing/rate-limit tiers:
- **Free tier**: Lowest limits, often 3-5 requests/min or ~40k tokens/month
- **Pay-as-you-go**: Higher limits that scale with spending
- **Enterprise**: Custom limits via contracts

### Token-Based Rate Limits
Rather than request counts, providers typically throttle by tokens/minute (TPM):
- Input + output tokens count toward the same limit
- Example: 90k TPM tier means 90,000 tokens consumed per minute, not requests
- Allows larger requests if you stay within the window

### Common Retry Headers
Standard HTTP headers for rate limit info:
- `RateLimit-Remaining-Tokens`: Tokens available in current window
- `RateLimit-Reset-Tokens`: Unix timestamp when tokens reset
- `Retry-After`: Seconds to wait before retrying
- `X-RateLimit-*` variants (non-standard but common)

### Retry Behavior Best Practices
- **Exponential backoff**: Wait 1s, 2s, 4s, 8s before retries
- **Jitter**: Add randomness to prevent thundering herd
- **429 status code**: Universal "too many requests" response

---

## What You Must Verify Per Provider

### Specific Limits
- [ ] Exact TPM for your chosen tier (OpenAI, Anthropic, and others differ)
- [ ] Requests per minute (if they impose this as a *separate* limit)
- [ ] Daily/monthly quotas (some providers have them, others don't)
- [ ] If limits differ by model (newer models often have lower initial limits)

### Rate Limit Headers
- [ ] Which header names they actually use (naming varies)
- [ ] Whether they include all standard headers or a subset
- [ ] If they provide `Retry-After` or only `RateLimit-Reset-*`

### Soft vs. Hard Limits
- [ ] Whether bursting slightly above limits is tolerated
- [ ] How quickly they enforce (immediate rejection vs. queue-based)
- [ ] If there's a "burst capacity" window separate from sustained TPM

### Increase Procedures
- [ ] How to request higher limits (some auto-increase, others require contact)
- [ ] How long increases take to process
- [ ] Whether limits increase based on usage/spend or require manual application

### Account-Level Details
- [ ] If limits apply per API key, per account, or per organization
- [ ] Whether concurrent requests count separately
- [ ] If batch/async APIs have different limits

---

## Practical Verification Checklist

```
Provider: _______________
Model: ___________________

○ Reviewed official rate limit documentation (not blogs/Reddit)
○ Checked current pricing page (limits change)
○ Tested actual response headers with a real request
○ Noted any model-specific limit variations
○ Confirmed how to monitor current usage (dashboards exist?)
○ Tested retry behavior with a small throttle
○ Verified if organization has special agreements
```

---

## Red Flags in Docs

⚠️ **If provider documentation doesn't clearly specify:**
- Don't assume it's unlimited
- Don't rely on third-party summaries
- Contact their support with a specific test

This is worth 15 minutes of checking before building production logic around rate limits.