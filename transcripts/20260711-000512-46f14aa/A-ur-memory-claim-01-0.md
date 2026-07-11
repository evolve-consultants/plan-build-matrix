# LLM Provider API Rate Limits: General Patterns

## General Knowledge (fairly consistent across providers)

**Rate limit dimensions** are typically measured across several axes simultaneously:
- **RPM** (Requests Per Minute) — how many API calls you can make
- **TPM** (Tokens Per Minute) — combined input + output tokens processed
- **TPD** (Tokens Per Day) — some providers add daily caps too
- **Concurrent requests** — max simultaneous in-flight requests

You're usually bound by whichever limit you hit first, not all of them equally.

**Tier systems** are common:
- Providers often gate higher limits behind usage/spend history or manual approval
- Typical progression: free/trial tier → pay-as-you-go tier 1 → higher tiers unlocked by cumulative spend or time-since-signup
- Higher tiers unlock higher RPM/TPM, sometimes access to specific models

**Retry/backoff conventions**:
- 429 status code = rate limit exceeded (this is near-universal, HTTP standard)
- `Retry-After` header is common but not guaranteed — tells you how long to wait
- Exponential backoff with jitter is the standard client-side strategy
- Some APIs return current usage/remaining quota in response headers (e.g., `x-ratelimit-remaining-requests`, `x-ratelimit-remaining-tokens`) — pattern is common but header names vary

**Other common patterns**:
- Rate limits are usually per-API-key or per-organization, not per-IP
- Streaming responses sometimes count tokens differently than non-streaming
- Batch APIs often have separate, more generous limits than real-time endpoints

---

## What You Should Verify for Your Specific Provider

⚠️ These vary significantly and change over time — don't rely on my memory for exact numbers:

- **Exact RPM/TPM values per tier** — these are frequently updated and differ wildly by provider and model
- **Exact header names** for rate limit info (naming conventions differ)
- **Whether `Retry-After` is in seconds vs. a timestamp**
- **How tiers are calculated** (spend thresholds, time-based, manual request) and current tier thresholds
- **Whether limits are per-model, per-endpoint, or account-wide**
- **Whether there's a distinction between input/output token limits** (some separate these, most combine)
- **Enterprise/custom limit availability** — often undocumented, negotiated directly
- **Current 429 response body format** — error message structure/fields differ

---

**Practical suggestion:** Check the provider's live rate-limit documentation page and inspect actual response headers from a test call — these are the two sources of truth, since this is one of the most frequently updated parts of any provider's API.