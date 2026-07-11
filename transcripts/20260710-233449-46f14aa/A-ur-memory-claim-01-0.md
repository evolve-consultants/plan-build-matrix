# API Rate Limits for LLM Providers

## General Architecture (Standard Across Most Providers)

### Tier Structure
**General knowledge:** Most LLM providers use tiered rate limiting:
- **Free/trial tier**: Most restrictive (often 3-100 requests/min)
- **Pay-as-you-go**: Moderate limits (typically 3,500-90k tokens/min)
- **Enterprise**: Custom, negotiated limits

### Token-Based vs Request-Based Limits
**General knowledge:** Providers use both metrics:
- **Tokens Per Minute (TPM)**: The dominant limit—counts input + output tokens
- **Requests Per Minute (RPM)**: Secondary limit—total API calls allowed
  - Example: You might hit 90k TPM OR 3,500 RPM first, whichever comes first

### HTTP Response Headers
**General knowledge:** Standard rate limit signaling:
```
RateLimit-Limit-Tokens: 90000
RateLimit-Remaining-Tokens: 45000
RateLimit-Reset-Tokens: 2024-01-15T10:30:00Z

RateLimit-Limit-Requests: 3500
RateLimit-Remaining-Requests: 2800
RateLimit-Reset-Requests: 2024-01-15T10:30:00Z
```

### Retry Behavior
**General knowledge:** Standard HTTP patterns:
- **429 status code**: "Too Many Requests"
- **Retry-After header**: Seconds to wait before retrying
- **Exponential backoff**: Industry-standard retry strategy (wait 1s, 2s, 4s, 8s...)

---

## What You MUST Verify Per Provider

### Critical Variables (Check Documentation)
- [ ] **Exact TPM limits** by tier (varies wildly: OpenAI vs Claude vs others)
- [ ] **Exact RPM limits** (some providers don't enforce this)
- [ ] **Header names** (some use non-standard formats)
- [ ] **Burst capacity** (some allow temporary overages)
- [ ] **Reset window** (typically 1 minute, but verify)
- [ ] **Retry-After format** (seconds vs milliseconds vs HTTP-date)

### Provider-Specific Quirks to Check
| Aspect | Why It Varies |
|--------|---------------|
| **Batch processing discounts** | Some providers offer separate batch APIs with no/different limits |
| **Fallback behavior** | Does queuing happen automatically, or do you get rejected? |
| **Shared vs dedicated limits** | Do all org members share one pool or get individual limits? |
| **Upgrade propagation time** | How long after upgrading tier do new limits apply? |
| **Soft vs hard limits** | Some providers warn before hard cuts |

---

## Example: How to Find This Information

**Where to verify:**
1. Provider's official documentation (usually API reference → Rate Limits section)
2. Dashboard/billing page (often shows current limits)
3. Header inspection (make a real request, check response headers)
4. Support documentation (edge cases, burst limits, enterprise options)

**Red flags if unclear:**
- Documentation doesn't specify TPM vs RPM
- No mention of retry header or reset timing
- Different limits listed in different docs (use most recent)

---

## Implementation Checklist

- [ ] Read provider's rate limit docs (record exact numbers)
- [ ] Implement header parsing for your specific provider's format
- [ ] Test 429 responses in staging with real retry headers
- [ ] Verify reset window timing with test requests
- [ ] Check if batch/async endpoints have different limits
- [ ] Confirm behavior under burst (sustained vs. momentary overages)

**Always test assumptions with small real requests rather than guessing.**