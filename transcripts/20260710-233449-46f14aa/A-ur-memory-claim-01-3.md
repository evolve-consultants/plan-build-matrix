# LLM API Rate Limits: How They Work

## General Knowledge (Industry Standard Patterns)

### Common Tier Structure
- **Free tier**: Lowest limits, often 3-10 requests/minute
- **Paid tiers**: Graduated by subscription level (e.g., Pro, Enterprise)
- **Usage-based**: Pay per token, with soft limits before throttling
- **Enterprise**: Custom limits negotiated per contract

### Token-Based Limits (Most Common)
- Limits expressed as **tokens per minute (TPM)** rather than requests
- Example: 90,000 TPM on a standard tier
- Applies to input + output tokens combined (verify which for your provider)
- Separate limits sometimes exist for input-only vs. total

### Request Rate Limits
- Separate from token limits (e.g., 3,500 requests/minute)
- Prevents hammering API even with small requests
- Lower than you'd expect if optimizing batch sizes

### Standard Retry Headers
```
Retry-After: 60  (seconds to wait before retrying)
X-RateLimit-Limit-Requests: 3500
X-RateLimit-Limit-Tokens: 90000
X-RateLimit-Remaining-Requests: 3499
X-RateLimit-Remaining-Tokens: 89950
X-RateLimit-Reset-Requests: 2024-01-15T12:34:00Z
X-RateLimit-Reset-Tokens: 2024-01-15T12:34:30Z
```

### Error Responses
- **HTTP 429**: Rate limit exceeded
- **HTTP 503**: Capacity issue (related but distinct)
- Response body typically indicates which limit was hit

### Quota vs. Rate Limit (Important Distinction)
- **Rate limit**: Per-minute throughput (resets frequently)
- **Quota**: Monthly/daily spend cap (different reset cadence)
- Both can stop your API calls

---

## What You MUST Verify for Your Specific Provider

### 1. **Limit Calculation Method**
- [ ] Do output tokens count toward TPM limit?
- [ ] Are prompt caching tokens counted differently?
- [ ] Is there a separate embedding rate limit?
- [ ] Do retries consume quota twice?

### 2. **Which Headers Are Actually Sent**
Different providers use different header names:
- OpenAI: `x-ratelimit-*-remaining`
- Anthropic: May use different format
- Others: Custom implementations
- **Test**: Make an actual API call and inspect response headers

### 3. **Tier Specifics**
- [ ] What are the exact TPM limits for your tier?
- [ ] Are there separate limits per model?
- [ ] Do limits differ by region?
- [ ] Can you burst above the minute limit briefly?

### 4. **Reset Timing**
- [ ] Is the minute a rolling window or fixed window?
- [ ] How are resets communicated (header timestamp vs. Retry-After)?
- [ ] What's the actual reset clock accuracy?

### 5. **Soft vs. Hard Limits**
- [ ] Does provider warn before hard limit?
- [ ] Are there grace periods or gradual throttling?
- [ ] Can you request temporary increases?

### 6. **Batch/Async Endpoints**
- [ ] Do batch requests use different limits?
- [ ] Are async jobs rate-limited differently?
- [ ] Can batching help you avoid per-minute limits?

### 7. **Multi-Model Limits**
- [ ] Does each model have its own limit?
- [ ] Do cheaper models share quota with expensive ones?
- [ ] Are vision/embedding models separate?

---

## Practical Verification Checklist

**Before Production:**
```python
# 1. Check documentation at:
#    - API reference for your specific tier
#    - Pricing page (often lists TPM)
#    - Status page for current limits

# 2. Test with real request:
import requests
response = requests.get("https://api.provider.com/v1/models")
print(response.headers)  # Look for x-ratelimit-* or similar

# 3. Monitor for 429 responses in staging
# 4. Implement exponential backoff with Retry-After header
# 5. Contact provider support for:
#    - Any discrepancies in documentation
#    - Custom limits if needed
#    - Confirmation of burst behavior
```

---

## Red Flags / Things Often Misunderstood

⚠️ **Common Mistakes:**
- Assuming output tokens are "free" (they usually aren't)
- Not reading the fine print on tier downgrade resets
- Treating rate limit headers as authoritative without testing
- Forgetting that quota and rate limits reset on different schedules
- Not accounting for retries in your quota consumption math

**Next step:** Link to your provider's documentation so I can help you verify the specific details.