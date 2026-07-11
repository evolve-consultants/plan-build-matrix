# LLM API Rate Limiting: How It Typically Works

## General Pattern (Most Providers)

### Tier-Based Structure
- **Free tier**: Lower limits (often 3-10 requests/min, ~90k tokens/month)
- **Pay-as-you-go**: Moderate limits that scale with usage (~3,500 tokens/min typical)
- **Enterprise**: Custom limits negotiated directly

### Token-Based Limits
Most providers track both:
- **Requests per minute (RPM)**: Number of API calls allowed
- **Tokens per minute (TPM)**: Total token throughput (input + output)

Example: "3,500 TPM, 200 RPM" means you're constrained by whichever hits first.

### HTTP Response Headers (Standard)
Providers typically return:
- `x-ratelimit-limit-requests`: Max requests in window
- `x-ratelimit-limit-tokens`: Max tokens in window
- `x-ratelimit-remaining-requests`: Still available
- `x-ratelimit-remaining-tokens`: Still available
- `x-ratelimit-reset-requests`: Unix timestamp when requests reset
- `x-ratelimit-reset-tokens`: Unix timestamp when tokens reset

### Retry Behavior (Expected)
- **429 status code**: Rate limit exceeded
- **Exponential backoff**: Wait 1s, 2s, 4s, 8s...
- **Retry-After header**: Seconds to wait (may be present)
- **Soft limits**: Gradual slowdown before hard rejection (common)

---

## What You MUST Verify Per Provider

| Aspect | Why It Varies | Example Differences |
|--------|---------------|-------------------|
| **Limit metrics** | Some use tokens only, others add requests | OpenAI uses TPM+RPM; some use TPM only |
| **Reset window** | Minute boundaries vary | Calendar minute vs. rolling 60s |
| **Burst capacity** | Unused quota carryover differs | Some allow overage in next window; others don't |
| **Header names** | No universal standard | May use `x-ratelimit-*` or `ratelimit-*` or custom names |
| **Upgrade paths** | Scaling rules vary dramatically | One provider: auto-upgrade after 7 days; another: manual request only |
| **Shared vs. org limits** | Quota allocation differs | Limit per API key vs. per organization vs. per project |

### Critical Provider-Specific Questions

**Check each provider's docs for:**

1. **How are limits applied?**
   - Per API key? Per organization? Per user account?
   - Are they shared across team members?

2. **What's the reset cadence?**
   - Rolling window or calendar-based?
   - Exactly when does a "minute" reset?

3. **How do input vs. output tokens count?**
   - Usually 1:1, but verify
   - Do system prompts count? Context caching implications?

4. **What happens at the limit?**
   - Immediate 429? Queuing? Gradual throttling?
   - Can you exceed briefly then pay later?

5. **Batch/async APIs different?**
   - Often have separate, higher limits
   - May use different quota buckets

6. **Rate limit headers present?**
   - Not guaranteed; check if available
   - If present, what do they actually name/calculate?

---

## Practical Implementation Checklist

✅ **Do this for any LLM provider:**
- [ ] Log actual response headers from a few test calls
- [ ] Test what happens at the limit (live testing, small scale)
- [ ] Read their specific rate limit documentation fully
- [ ] Check if there's a status page for limit incidents
- [ ] Verify limit behavior in their SDK (may differ from raw API)
- [ ] Confirm burst vs. sustained behavior expectations

❌ **Don't assume:**
- That header names match documentation
- That limits are strictly enforced uniformly
- That unused quota rolls over
- That the limit window is exactly 60 seconds

---

## Quick Verification Template

```
Provider: [Name]
Source: [Link to their rate limit docs]

Limits:
- Requests/min: ____ (confirmed by: ____)
- Tokens/min: ____ (confirmed by: ____)
- Reset window: ____ (rolling/calendar/other)

Headers present: [ ] Yes [ ] No [ ] Partial
- List: ____________

Burst behavior: __________
Upgrade path: __________
```

Most providers follow the general pattern above, but the devil is in these specific details—especially for production systems where hitting limits causes real issues.