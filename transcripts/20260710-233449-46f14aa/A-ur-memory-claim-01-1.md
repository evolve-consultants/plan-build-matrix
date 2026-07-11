# API Rate Limits for LLM Providers

## General Knowledge (Standard Across Industry)

### Common Tier Structure
- **Free tier**: Most restrictive; often 3-5 requests/minute, lower token allowances
- **Paid tiers**: Graduated by price; correlate spending level to rate limits
- **Enterprise**: Custom limits negotiated per contract

### Token-Based Limits
- Measured in **tokens per minute (TPM)**, not requests
- Separate limits often exist for:
  - Input tokens/minute
  - Output tokens/minute
  - Total tokens/minute
- More granular than request counting; accounts for actual computational cost

### Standard HTTP Headers (RFC 6585)
```
Rate-Limit-Limit: 1000000          # Total allowed in window
Rate-Limit-Remaining: 999950       # Tokens/requests left
Rate-Limit-Reset: 1234567890       # Unix timestamp when limit resets
Retry-After: 45                    # Seconds to wait before retrying (429 response)
```

### Typical Retry Logic
- **429 Too Many Requests**: Standard rate limit error
- **503 Service Unavailable**: May also indicate throttling
- Exponential backoff recommended (wait 2^n seconds, capped at some max)
- Respect `Retry-After` header if present

### Batch Processing Strategies (General)
- Request queuing with delays
- Concurrent request management (respecting simultaneous request limits)
- Preferring batch endpoints if available (often have different rate limits)

---

## Provider-Specific (Verify Before Implementation)

### You MUST Check For Each Provider:

**Rate Limit Specifics**
- [ ] Exact TPM/RPM for each tier you're using
- [ ] Whether input/output tokens have separate limits
- [ ] If there are per-model differences (GPT-4 vs GPT-3.5, Claude 3 vs Claude 3.5, etc.)
- [ ] Reset window duration (typically 1 minute, but verify)

**Header Names**
- [ ] Exact header names they use (some use non-standard variants)
- [ ] Whether they include all standard headers
- [ ] How they communicate remaining quota

**Throttling Behavior**
- [ ] Do they gradually throttle or hard-stop at limit?
- [ ] What errors indicate rate limiting specifically?
- [ ] Are there burst allowances above sustained TPM?

**Batch/Async Endpoints**
- [ ] Different rate limits for batch APIs?
- [ ] Whether batch jobs count against live API limits?
- [ ] Pricing implications

**Specific Cases to Verify**
- [ ] Behavior during scale-up (do limits increase smoothly?)
- [ ] Whether concurrent requests have separate limits from TPM
- [ ] If streaming responses count tokens differently
- [ ] Organization/account-level vs project-level limits

### Key Providers (Examples of Variation)

| Provider | Known Pattern | Must Verify |
|----------|---------------|------------|
| **OpenAI** | Separate input/output TPM | Model-specific limits, organization tiers |
| **Anthropic** | Single TPM limit | Batch API rate limits, tier progression |
| **Google (Gemini)** | RPM + TPM | Regional differences, quota adjustments |
| **Cohere** | Tiered by plan | Whether chat has different limits than completions |

---

## Implementation Checklist

```
□ Get exact rate limit numbers from provider docs
□ Log actual header values in first test requests
□ Implement header parsing (not hardcoded assumptions)
□ Test retry logic with intentional rate limit hits
□ Monitor actual reset times (may differ from documented)
□ Set up alerts for approaching limits
□ Document your provider's specific behavior
□ Re-verify after any tier changes
```

---

**Golden Rule**: Provider documentation is your source of truth. This summary describes *general patterns*, but enforcement and communication mechanisms vary enough that assuming consistency across providers is a common bug source.