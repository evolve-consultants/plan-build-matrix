**Operating from: Upper-Right (Build + Verify)**

### Confirming before I proceed

I'm treating this as a general education request about rate-limiting mechanics, not a guide to a specific provider's implementation. I'm assuming you want to understand the *pattern* so you can interpret any provider's docs correctly.

---

## How LLM API Rate Limits Work

### Tier Structure (General Knowledge)

Most LLM providers use **paid tiers** that correlate rate limits to subscription level:

| Tier | Typical Rate Limit | Use Case |
|---|---|---|
| Free / Trial | 3–20 requests/min, low total monthly tokens | Testing, prototyping |
| Starter / Pro | 90–180 requests/min, 1–2M tokens/month | Small production apps |
| Business / Enterprise | 500+ req/min, custom token pools, priority queuing | High-volume, mission-critical |

**Key principle**: limits exist to prevent resource exhaustion and ensure fair allocation across all users on shared infrastructure.

---

### Token-Based Limits (General Knowledge)

Most providers implement **dual limits**:

1. **Requests Per Minute (RPM)** — how many API calls you can make
2. **Tokens Per Minute (TPM)** — the actual throughput ceiling

You can hit either limit first. Example:
- Tier allows 90 requests/min and 90,000 tokens/min
- If your average request is 1,500 tokens, you hit TPM after ~60 requests
- If your average request is 500 tokens, you hit RPM after 90 requests

**Verify for your provider**: which limit is tighter for your typical request size.

---

### Retry Headers (Externally Verifiable)

When you exceed rate limits, the provider returns **HTTP 429** (Too Many Requests) with headers:

```
HTTP/1.1 429 Too Many Requests
Retry-After: 30
X-Ratelimit-Limit-Requests: 90
X-Ratelimit-Remaining-Requests: 0
X-Ratelimit-Remaining-Tokens: 0
X-Ratelimit-Reset-Requests: 2024-01-15T14:32:00Z
X-Ratelimit-Reset-Tokens: 2024-01-15T14:32:15Z
```

| Header | Meaning | Action |
|---|---|---|
| `Retry-After` | Seconds to wait before retrying | Wait at least this long; don't retry sooner |
| `X-Ratelimit-Remaining-*` | Budget left in current window | Tells you how close you are to the next limit |
| `X-Ratelimit-Reset-*` | When the limit resets | Useful for scheduling batch jobs |

**General pattern**: always respect `Retry-After`. Exponential backoff (wait 1s, then 2s, then 4s) is safe if the header isn't present, but headers are always more reliable.

---

### Rate-Limit Windows (General Knowledge)

Limits reset on a **rolling or fixed window**:

- **Rolling minute**: counts the last 60 seconds of requests at any moment (more common)
- **Fixed minute**: resets at the top of each calendar minute (easier to hit unexpectedly)

**Verify for your provider**: most use rolling, but check their docs.

---

### Hard vs. Soft Limits (General Knowledge)

- **Hard limit**: API rejects the request immediately with 429
- **Soft limit**: may be warnings in response headers; you haven't hit the ceiling yet but are close

Some providers expose `X-Ratelimit-Remaining-*` to let you implement soft-limit backoff *before* hitting the hard limit.

---

## What to Verify for Your Specific Provider

Before integrating, check their documentation for:

1. **Exact tier names and rate limits** — naming varies widely (OpenAI: "rate limit tiers"; Anthropic: "usage tiers")
2. **How TPM is calculated** — some count input + output tokens equally; others weight them differently
3. **Separate limits for different endpoints** — some providers have per-model rate limits or different ceilings for chat vs. embeddings vs. batch APIs
4. **Batch API exceptions** — many providers offer async batch endpoints with much higher effective throughput but different pricing
5. **Header names** — the `X-Ratelimit-*` headers above are common but not universal; some providers use slightly different names
6. **Reset timing precision** — does it reset per minute or per hour? Some (like Anthropic) have separate daily limits too
7. **Retry behavior** — whether they recommend exponential backoff, jitter, or just respecting `Retry-After`

**Quick checklist**:
- [ ] Find the rate-limit page in your provider's docs
- [ ] Test against the rate limit in a staging environment (usually safe)
- [ ] Log the headers you receive on a real 429 to see what fields are actually present
- [ ] Compare your typical request size against the TPM limit to see which constraint is tighter

---

## Implementation Pattern (General Knowledge)

A production retry loop should:

```
1. Make request
2. If 429:
   a. Parse Retry-After header (or use exponential backoff)
   b. Wait
   c. Retry
3. Track X-Ratelimit-Remaining-* to implement soft-limit backoff
   (pause if remaining budget is low, don't wait for 429)
```

This avoids unnecessary hard failures and keeps your app responsive under load.