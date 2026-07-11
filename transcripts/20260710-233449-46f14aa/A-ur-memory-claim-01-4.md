# API Rate Limits for LLM Providers

## General Knowledge (Industry Standard Patterns)

### Common Tier Structure
- **Free/Trial**: Lowest limits, often restrictive (e.g., 3-10 requests/min)
- **Pay-as-you-go**: Medium limits that scale with usage or account age
- **Pro/Dedicated**: Higher limits, sometimes customizable
- **Enterprise**: Negotiated custom limits, often including reserved capacity

### Token-Based Limits
Most providers implement **tokens per minute (TPM)** rather than requests/minute:
- Input tokens and output tokens both count
- Limits are often asymmetric (e.g., lower output TPM than input)
- Separate limits for different model families (GPT-4 vs GPT-3.5, Claude 3 Opus vs Haiku)
- Total account limits plus per-model limits

### HTTP Response Headers (Standard Pattern)
```
RateLimit-Limit-Requests: 10000
RateLimit-Limit-Tokens: 2000000
RateLimit-Remaining-Requests: 9999
RateLimit-Remaining-Tokens: 1999500
RateLimit-Reset-Requests: 2024-01-15T12:35:00Z
RateLimit-Reset-Tokens: 2024-01-15T12:35:00Z
```

### Retry Strategy (Best Practice)
- **429 (Too Many Requests)** indicates rate limit exceeded
- Use **exponential backoff** with jitter (standard: 2^n seconds, add random jitter)
- Respect `Retry-After` header if provided (can be seconds or HTTP-date)
- Most providers recommend starting with 1-5 second wait, max ~60 seconds

---

## **VERIFY FOR YOUR SPECIFIC PROVIDER**

### Critical Details to Confirm
- [ ] Exact TPM and RPM limits for each tier and model
- [ ] How tokens are counted (do system prompts count? Cached tokens different?)
- [ ] Whether limits are:
  - Per-minute (rolling window) or per-second
  - Per-account or per-API-key
  - Hard stops vs soft throttling
- [ ] Specific header names and formats (may vary significantly)
- [ ] Reset behavior:
  - Do unused tokens roll over?
  - Is there a daily budget that resets?
- [ ] Burst allowances (can you exceed momentarily?)
- [ ] How to request limit increases
- [ ] Batch API availability (cheaper for non-real-time requests)

### Where to Check
- **Official documentation**: Rate limits page (usually clearly stated)
- **API response headers**: Live inspect what your provider actually returns
- **Dashboard**: Many providers show current usage and limits
- **Status page**: Some publish aggregate rate limit information
- **Support**: Custom limits require contacting sales/support

---

## Common Provider-Specific Variations

| Aspect | Why It Varies |
|--------|---------------|
| Token counting | Different tokenizers; some count special tokens |
| Reset windows | 1-min rolling, 1-min fixed, hourly, or daily budgets |
| Concurrency limits | Some cap simultaneous requests separately |
| Queue behavior | Some queue requests, others reject immediately |
| Billing impact | Rate limiting may or may not charge for rejected requests |

**Bottom line**: The general principles above apply broadly, but rate limits are one of the areas where provider implementations differ most. Always verify against current documentation before building production systems.