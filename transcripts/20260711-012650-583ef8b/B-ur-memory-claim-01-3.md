**Operating from: Upper-Right (Build + Verify)**

### Confirming before I proceed
- You want a **general overview** of how rate limiting works across the LLM industry, not a guide for a specific provider (which would require current documentation)
- You understand this will be accurate in structure and mechanism but may be dated or incomplete in specific numbers
- You're comfortable with inline uncertainty markers showing what to verify

---

## General Structure of LLM Rate Limits

### Tier-Based Limits (General Knowledge)

Most LLM providers use **subscription tiers** that gate three kinds of limits:

| Tier | Typical Use | Rate Limit Model |
|---|---|---|
| **Free/Trial** | Testing, low volume | Very restrictive; often includes request-count limits (e.g., 100 requests/day) plus token limits |
| **Standard/Pay-as-you-go** | Production use, variable load | Token-per-minute (TPM) limits; sometimes request-per-minute (RPM) limits as secondary gates |
| **Pro/Enterprise** | High volume, SLA needs | Higher TPM/RPM; sometimes custom limits negotiated per contract |

**What to verify**: The specific tier names, thresholds, and whether your provider uses RPM limits at all. (Some use only TPM; others use both.)

---

### Tokens Per Minute (TPM) — The Primary Limit (General Knowledge)

**How it works:**
- The provider counts both **input tokens** (your prompt) and **output tokens** (the model's response)
- They accumulate within a rolling 60-second window
- Once you hit the TPM limit, further requests are rejected until the window resets

**Example (General):**
```
Standard tier: 100,000 TPM
Your request uses 1,500 input + 500 output = 2,000 tokens
Remaining budget this minute: 98,000 tokens
```

**What to verify**: 
- Exact TPM limit for your tier
- Whether both input and output count equally, or if output tokens are weighted differently
- Whether the window is truly rolling or reset at fixed intervals

---

### Requests Per Minute (RPM) — Secondary Limit (General Knowledge)

Some providers also cap **how many API calls** you can make, independent of token count:

```
Example: 500 RPM limit
Even if you have TPM budget left, the 500th request in a minute is rejected.
```

**What to verify**: Whether your provider uses RPM limits at all, and if so, whether they're listed in the same documentation as TPM limits (they sometimes are, sometimes aren't).

---

### Rate Limit Response Headers (General Knowledge)

When you hit a limit, the provider returns HTTP headers that tell you:

| Header | Meaning | Example |
|---|---|---|
| `x-ratelimit-limit-tokens` | Your TPM ceiling | `100000` |
| `x-ratelimit-remaining-tokens` | Tokens left this minute | `45230` |
| `x-ratelimit-reset-tokens` | Unix timestamp when window resets | `1699564890` |
| `retry-after` | Seconds to wait before retrying | `15` |

**What to verify**: 
- The exact header names (they vary by provider; some use `rate-limit-*`, others use `x-ratelimit-*`)
- Whether all these headers are present in every response or only when near limits

---

### HTTP Status Codes for Rate Limit Events (General Knowledge)

| Status | Meaning | Typical Behavior |
|---|---|---|
| `429 Too Many Requests` | You've hit a rate limit | Includes `retry-after` header; you should backoff and retry |
| `503 Service Unavailable` | Temporary overload (sometimes rate-limit-adjacent) | Often includes `retry-after`; treat similarly to 429 |

**What to verify**: Whether your provider uses 429, 503, or both. (Most use 429; some older systems use 503.)

---

### Retry Strategies (General Knowledge)

**Standard practice:**
1. **Check `retry-after` header** — use the time it specifies (this is the only reliable signal)
2. **Exponential backoff** — if no header, wait 2^n seconds (1, 2, 4, 8, 16…) up to a cap (usually 60–120s)
3. **Jitter** — add randomness to avoid thundering herd if multiple clients hit limits simultaneously
4. **Max retries** — give up after N attempts (typically 3–5) to avoid infinite loops

**Pseudocode (General):**
```python
attempt = 0
max_attempts = 5

while attempt < max_attempts:
    try:
        response = call_api()
        return response
    except RateLimitError as e:
        attempt += 1
        wait_time = e.retry_after or (2 ** attempt)
        wait_time += random.uniform(0, 1)  # jitter
        sleep(wait_time)
```

**What to verify**: Whether your provider's SDK implements this, or if you need to handle it yourself. (Most modern SDKs handle it automatically.)

---

### Burst vs. Steady-State Limits (General Knowledge)

Some providers distinguish:
- **Burst limit**: how many tokens you can use in a single request (sometimes lower than you'd expect)
- **Sustained limit**: your per-minute average

**Example (hypothetical):**
```
TPM limit: 100,000
Max tokens per single request: 10,000
```

This means you can't send one 20,000-token request even if you have budget.

**What to verify**: Whether your provider publishes per-request limits separately. (Not all do; many just use TPM as the only gate.)

---

### What Counts Against Limits (General Knowledge)

- **Input tokens**: Always counted
- **Output tokens**: Always counted (both in your quota and billing)
- **Cached tokens** *(some providers)*: May be counted at a reduced rate or not at all — major variation here
- **System prompts**: Counted as input tokens

**What to verify**: Especially the caching behavior if you're using prompt caching. This is a competitive differentiator and varies wildly.

---

## Summary Table: General vs. Verify

| Aspect | Known (General) | Verify for Your Provider |
|---|---|---|
| Rate limits are per-minute | ✓ | — |
| Limits use TPM as primary gate | ✓ | Confirm they don't use only request count |
| 429 + `retry-after` header is standard | ✓ | Confirm exact header names |
| Exponential backoff is best practice | ✓ | Check if SDK does it for you |
| Input + output tokens both count | ✓ | Confirm weighting (if any asymmetry) |
| Tier thresholds and names | — | ✗ Verify against current pricing page |
| Whether per-request limits exist | — | ✗ Check docs |
| Caching token behavior | — | ✗ Check docs (critical if you use it) |
| Exact header names in responses | — | ✗ Test a live request and inspect headers |

---

## Next Steps

If you're building a client or integrating with a specific provider:
1. **Get current docs**: Check their API reference for tier limits and header names
2. **Test it**: Make a request, hit the limit intentionally, capture the full response headers
3. **Confirm caching**: If you use prompt caching, verify how it affects TPM accounting
4. **Implement backoff**: Use your SDK's built-in retry logic, or implement exponential backoff + jitter

Is there a specific provider you're working with, or a specific scenario (e.g., batch processing, real-time streaming) where rate limits are a concern?