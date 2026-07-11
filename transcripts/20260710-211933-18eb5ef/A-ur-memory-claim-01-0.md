# LLM API Rate Limiting: General Structure

## **General Knowledge (Industry Standard Patterns)**

### Tier-Based Limits
Most providers use subscription tiers with increasing quotas:

| Tier | Typical Structure |
|------|-------------------|
| Free | Very restrictive (e.g., 3 requests/min, 90k tokens/day) |
| Pro/Standard | Moderate (e.g., 100k tokens/min) |
| Enterprise | Custom negotiation; usage-based billing |

### Rate Limit Dimensions
Providers typically track multiple metrics simultaneously:
- **Requests per minute (RPM)** — number of API calls
- **Tokens per minute (TPM)** — input + output tokens combined
- **Daily/monthly quotas** — aggregate caps
- **Concurrent requests** — simultaneous API connections

### Standard HTTP Headers (Verify Per Provider)
```
Rate-Limit-Limit-Requests: 100
Rate-Limit-Limit-Tokens: 90000
Rate-Limit-Remaining-Requests: 42
Rate-Limit-Remaining-Tokens: 45000
Rate-Limit-Reset-Requests: 1234567890
Rate-Limit-Reset-Tokens: 1234567895
Retry-After: 5  (seconds to wait before retry)
```

Header names **vary significantly** — some providers use `X-RateLimit-`, others use `RateLimit-`.

## **What You MUST Verify for Your Specific Provider**

### Critical Documentation Points
- [ ] Exact header names (not standardized across industry)
- [ ] Whether TPM includes both input and output tokens equally
- [ ] Batch vs. streaming endpoint limits (often different)
- [ ] Whether limits reset on fixed schedules or rolling windows
- [ ] Regional/geographic rate limit variations

### Retry Strategy Confirmation
- [ ] Does `Retry-After` header exist and what units (seconds/milliseconds)?
- [ ] Are 429 responses exponential backoff recommended?
- [ ] Do failed requests consume quota?
- [ ] Are there "burst" allowances above sustained limits?

### Provider-Specific Quirks
- [ ] OpenAI: Legacy separate RPM/TPM tracking; newer models may differ
- [ ] Anthropic: Sometimes uses different limits for different model families
- [ ] Google/Azure: May have project-level vs. quota-level limits
- [ ] Local/self-hosted: May have no rate limiting or custom implementations

## **Practical Verification Steps**

1. **Read current API docs** — this info changes quarterly for major providers
2. **Check dashboard/billing section** — limits often shown there with real-time usage
3. **Make test requests** — observe actual header responses in your environment
4. **Review status page** — some providers publish rate limit incidents
5. **Contact support for edge cases** — batch processing, large deployments

## **Implementation Red Flags**

These assumptions frequently cause problems:
- ❌ "All providers follow RFC 7231 rate limit headers" (they don't)
- ❌ "If I stay under TPM, I won't hit RPM limits" (often independent)
- ❌ "Errors don't consume quota" (depends on provider)
- ❌ "Reset times are always at midnight UTC" (usually rolling windows)

Would you like me to show how to extract and use these headers in actual code, or dig into any specific provider's documentation?