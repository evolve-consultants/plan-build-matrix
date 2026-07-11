**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You want a general summary of how LLM API rate limiting works across the industry — the common patterns, terminology, and mechanics — with clear signposting of what's universal versus what requires provider-specific verification before you rely on it in production.

<assumptions>
  <task>You're either building an integration or understanding rate limits for the first time, and you need enough context to read provider docs intelligently</task>
  <operator>You can verify facts by checking provider documentation; you want to know what to look for</operator>
  <project>No specific provider yet, or you're evaluating multiple</project>
</assumptions>

### What I'm unsure of
- Whether you need this for a specific provider (OpenAI, Anthropic, etc.) or a general framework
- Whether you're building a client library, monitoring system, or just understanding limits for operational planning
- Your risk tolerance: do you need to handle graceful degradation, or is basic backoff sufficient?

---

## General Rate Limiting Patterns (Standard Across Providers)

### Tier Structure
**General knowledge**: Nearly all providers use subscription or usage-based tiers that gate:
- **Requests per minute (RPM)** — how many API calls you can make
- **Tokens per minute (TPM)** — the total token budget across all requests
- **Concurrency limits** — simultaneous connections allowed

Example structure (typical):
- Tier 1 (free/trial): 3 RPM, 90K TPM
- Tier 2 (paid starter): 60 RPM, 1M TPM
- Tier 3 (paid scale): 500 RPM, 2M TPM

**Verify per provider**: Exact numbers, whether limits are soft/hard, and whether there's per-minute vs. per-day budgeting.

---

### How Limits Are Enforced
**General knowledge**: 
- Requests that exceed limits are rejected with an HTTP 429 (Too Many Requests) response
- Rate limits reset on a **sliding window** (most common) or **fixed window** (less common)
  - *Sliding window*: limit resets continuously; e.g., "3 requests per 60 seconds" means any rolling 60-second window
  - *Fixed window*: limit resets at clock boundaries; e.g., "3 per minute" resets at :00 of each minute
- Both RPM and TPM limits apply simultaneously — you hit whichever limit first

**Verify per provider**: Which windowing strategy they use (usually documented in rate limit headers).

---

### Retry Headers (The Standard Pattern)
**General knowledge**: When you hit a 429, the response includes headers to tell you when to retry:

```
HTTP/1.1 429 Too Many Requests

retry-after: 30
x-ratelimit-limit-requests: 60
x-ratelimit-limit-tokens: 1000000
x-ratelimit-remaining-requests: 0
x-ratelimit-remaining-tokens: 412000
x-ratelimit-reset-requests: 2024-01-15T14:30:45Z
x-ratelimit-reset-tokens: 2024-01-15T14:30:12Z
```

What these mean:
- **`retry-after`**: seconds to wait before retrying (HTTP standard)
- **`x-ratelimit-remaining-*`**: budget left in the current window (for requests and tokens)
- **`x-ratelimit-reset-*`**: when the limit resets (as a timestamp or seconds)
- **`x-ratelimit-limit-*`**: your tier's hard limits

**Verify per provider**: 
- Exact header names (some use `X-RateLimit-Reset-After`, others use timestamps, etc.)
- Whether they include *both* request and token headers (some only return one)
- Whether `retry-after` is always present or only on 429

---

### Proactive Monitoring (Before You Hit Limits)
**General knowledge**: Response headers on *successful* requests also include rate limit state:

```
HTTP/1.1 200 OK

x-ratelimit-remaining-requests: 45
x-ratelimit-remaining-tokens: 876000
x-ratelimit-reset-requests: 2024-01-15T14:30:45Z
```

This lets you:
- Track remaining budget in real time
- Implement backoff *before* hitting 429
- Plan batch sizes dynamically

**Verify per provider**: Whether these headers are included on 2xx responses (most do, some don't).

---

### Backoff Strategies (General Patterns)
**General knowledge**: Standard approaches:

| Strategy | How it works | Best for |
|----------|---|---|
| **Fixed backoff** | Wait 5s, retry. If 429 again, wait 10s. | Simple, low-concurrency clients |
| **Exponential backoff** | Wait 1s, then 2s, 4s, 8s... (capped). | Handling transient congestion |
| **Jitter** | Backoff + random delay to de-synchronize retries. | Preventing thundering herd (many clients retrying at once) |
| **Read retry-after header** | Always use the server's `retry-after` if present. | Most reliable; server knows its actual queue state |

**Verify per provider**: Whether they honor exponential backoff or prefer fixed/jittered retries.

---

## Provider-Specific Things to Verify

Create a checklist for whichever provider(s) you're using:

- [ ] **Exact rate limit values** for your tier (RPM, TPM, concurrency)
- [ ] **Header names** — do they use `x-ratelimit-` or `x-rate-limit-` or something else?
- [ ] **Window type** — sliding or fixed? Any documentation about how it works?
- [ ] **Retry behavior** — do they respect standard HTTP `retry-after`, or custom logic?
- [ ] **What resets when** — do RPM and TPM reset independently? At the same time?
- [ ] **Concurrency handling** — is there a separate limit, or is it enforced via token/request rate?
- [ ] **Burst allowance** — can you exceed limits briefly if you stay within the per-minute average?
- [ ] **Regional or account-level limits** — do different regions have different quotas?
- [ ] **Soft vs. hard limits** — do they warn before hard enforcement, or enforce immediately?

---

## Recommended Reading Order

1. **Start here**: Your provider's rate limit documentation (usually in their API docs under "Rate Limits" or "Quotas")
2. **Then**: Their HTTP response examples — copy the exact headers from their sample responses
3. **Then**: Their best practices guide (if they have one) — they often explain expected behavior in edge cases
4. **Finally**: Their status page or incident history — see if rate limits are a known failure mode

### Next prompt should include
- Which provider(s) you're integrating with
- What you're building (client library, batch processor, monitoring dashboard?)
- Whether you're handling the retry logic yourself or using an SDK (which usually bakes this in)

Then I can give you the provider-specific verification checklist and example implementations for your exact scenario.