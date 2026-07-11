# API Rate Limits for LLM Providers

## General Structure (Standard Across Industry)

### Tier System
- **Free tier**: Lowest limits, often 3-5 requests/minute
- **Pay-as-you-go**: Moderate limits scaling with usage/spend
- **Dedicated/Enterprise**: Custom limits negotiated per contract

Most providers use **tokens per minute (TPM)** as the primary constraint, not just requests, since token costs vary widely by model.

### Common Rate Limit Metrics
- **Requests per minute (RPM)**: Raw API calls
- **Tokens per minute (TPM)**: Sum of input + output tokens across all requests
- Often paired limits (e.g., "3,500 RPM AND 90,000 TPM")

### Standard HTTP Headers (RFC 6585 convention)
```
RateLimit-Limit-Requests: 3500
RateLimit-Limit-Tokens: 90000
RateLimit-Remaining-Requests: 3499
RateLimit-Remaining-Tokens: 89543
RateLimit-Reset-Requests: 1234567890
RateLimit-Reset-Tokens: 1234567891
```

### Retry Strategy (Best Practice)
- **429 status code**: Rate limit exceeded
- **Exponential backoff**: 1s → 2s → 4s → 8s (with jitter)
- **Retry-After header**: May specify wait time
- Most SDKs implement this automatically

---

## **⚠️ VERIFY WITH SPECIFIC PROVIDER** (varies significantly)

### Critical Details to Check
- **Exact tier names and limits** (pricing page + docs)
- **Header naming conventions** (some use different prefixes)
- **Reset window duration** (typically 1 minute, but not guaranteed)
- **Burst allowances** (can you exceed limits for <1s?)
- **How tokens are counted** (some only charge output tokens; streaming tokens counted differently)
- **Endpoint-specific limits** (image generation might have different caps than text)
- **Organization/project-level pooling** (do multiple API keys share a quota?)

### Examples of Variation
| Provider | Details to Verify |
|----------|---|
| OpenAI | Different limits per model; check [platform.openai.com/account/rate-limits](https://platform.openai.com/account/rate-limits) |
| Anthropic | Uses `anthropic-ratelimit-*` headers; tier-specific TPM varies widely |
| Google (Gemini) | Region-specific limits; quota management differs by model family |
| Local/Self-hosted | No rate limits (but watch your hardware) |

---

## Practical Implementation Checklist

✅ **Do check:**
- Your provider's pricing/documentation page (not blog posts)
- Dashboard/console for actual account limits
- SDK source code for default retry behavior
- Error responses from your specific tier

✅ **Do implement:**
- Logging of remaining quota from headers
- Exponential backoff on 429s
- Request queuing for predictable usage

❌ **Don't assume:**
- Headers match this template exactly
- Free tier limits are stable over time
- Shared org limits work intuitively
- Different models share the same limit pool

---

**Bottom line:** The *architecture* is standardized, but provider-specific limits and header formats require reading official docs—this is not something you should rely on intuition for.