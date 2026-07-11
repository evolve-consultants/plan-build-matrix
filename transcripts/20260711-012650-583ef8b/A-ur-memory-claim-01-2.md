# API Rate Limits for LLM Providers

## General Structure (Applies Broadly)

### Common Tier System
- **Free/Trial tier**: Most restrictive limits, sometimes with monthly quotas
- **Pay-as-you-go**: Per-minute and/or per-day limits tied to spending
- **Dedicated/Enterprise**: Custom limits negotiated per customer

### Token-Based Metrics
- **Tokens per minute (TPM)**: Primary limit for most providers
- **Requests per minute (RPM)**: Secondary limit (lower bound)
- **Concurrent requests**: Maximum simultaneous API calls
- **Examples**: TPM limits typically range from 90K–500K+ depending on tier

### Standard HTTP Headers
**Response headers you'll typically see:**
- `x-ratelimit-limit-requests`: Max RPM
- `x-ratelimit-limit-tokens`: Max TPM
- `x-ratelimit-remaining-requests`: Remaining for this window
- `x-ratelimit-remaining-tokens`: Remaining tokens
- `x-ratelimit-reset-requests`: Unix timestamp for RPM reset
- `x-ratelimit-reset-tokens`: Unix timestamp for TPM reset
- `retry-after`: Seconds to wait before retrying (on 429 response)

### Common Behaviors
- Rolling window (typically 1 minute)
- 429 (Too Many Requests) status code signals rate limit hit
- Exponential backoff is the standard retry pattern

---

## Provider-Specific (Verify Before Implementation)

### You Should Check For:

**OpenAI**
- Exact TPM/RPM for your specific model and tier
- Whether different models share quotas
- Batch API (different rate limit rules)

**Anthropic**
- Token window specifics (their rolling window implementation)
- Tier progression requirements and cost thresholds

**Google (Gemini), Meta (Llama), Cohere, Mistral**
- Whether they use TPM vs. other metrics
- Free tier existence and restrictions
- Whether rate limits are per-model or account-wide

**Self-hosted/Open models**
- Rate limiting may be entirely in your control
- May not follow standard conventions

### Implementation Specifics to Verify
- Exact header names (some providers use variations)
- Whether `retry-after` uses seconds or milliseconds
- Queuing behavior (do requests queue or fail immediately?)
- Whether burst capacity exists (temporary overage tolerance)
- Pricing impact of hitting limits (standard: you only pay for successful requests)

---

## Safe Implementation Strategy

**Do this for any provider:**
1. Read their current documentation (this changes)
2. Implement header parsing for their specific format
3. Test with a small request volume first
4. Use exponential backoff with `retry-after` guidance
5. Set alerts for approaching limits (typically at 70-80%)
6. Never hardcode limit assumptions