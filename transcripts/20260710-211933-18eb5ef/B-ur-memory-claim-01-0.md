**Operating from: Upper-Right (Build + Verify)**

### What I understand you're asking
A general overview of how LLM provider rate limits are structured, with enough specificity to be actionable, but clearly flagging what varies by provider so you know what to verify before relying on it.

<assumptions>
  <project>You're likely implementing client-side rate limit handling or planning API integration architecture</project>
  <task>You want a mental model of the landscape so you can read provider docs effectively and anticipate what you'll encounter</task>
  <operator>You own verification against actual provider docs before coding against these patterns</operator>
</assumptions>

---

## Rate Limit Architecture (General Knowledge)

### Tier-Based Quotas
Most LLM providers use a **tiered pricing model** where each tier (free, pro, enterprise) has its own rate limits:

- **Requests per minute (RPM)** — count of API calls, regardless of size
- **Tokens per minute (TPM)** — count of input + output tokens, the actual bottleneck for LLMs
- Some providers also cap **concurrent requests**

**Example structure** (this is representative but NOT universal):
| Tier | RPM | Input TPM | Output TPM |
|---|---|---|---|
| Free | 3 | 90,000 | 30,000 |
| Pro | 3,500 | 90,000,000 | 30,000,000 |
| Enterprise | Custom | Custom | Custom |

**You should verify**: exact numbers, whether limits are per-user or per-organization, and whether tiers have sub-limits (e.g., a max tokens per request even if daily allowance is high).

### Retry Headers
When you hit a rate limit, the provider returns **HTTP 429** (Too Many Requests) with headers that tell you when you can retry:

- **`Retry-After`** — seconds to wait before retrying (most reliable signal)
- **`RateLimit-Remaining`** — requests/tokens left in the current window
- **`RateLimit-Reset`** — Unix timestamp when the window resets
- **`RateLimit-Limit-Tokens-Per-Minute`** — your current TPM cap

**You should verify**: which headers each provider actually returns, whether `Retry-After` is in seconds or ISO 8601 format, and whether headers are present on success (many providers only send them on 429).

### Rate Limit Windows
Rate limits reset on a **sliding window** or **fixed window** (minute/hour boundaries):

- **Sliding window** (more common for token limits): limits apply to the last 60 seconds continuously; as requests age out, new ones can go through
- **Fixed window** (simpler, less fair): limits reset at fixed times (e.g., midnight UTC or top of each minute)

If you make 100 requests in the first 30 seconds of a minute-window, you're blocked for the next 30 seconds. With sliding windows, once 60 seconds pass from the first request, you can start making new ones.

**You should verify**: which windowing strategy each provider uses; it changes your backoff math.

---

## Standard Handling Patterns (General Knowledge)

### Exponential Backoff with Jitter
Standard client-side pattern:

```python
# Pseudocode
wait = min(base_delay * (2 ** attempt), max_delay) + random_jitter()
```

This prevents thundering herd: if 1000 clients all hit the limit at once and retry at the same time, they all fail again.

**You should verify**: what base delay to use (often 1 second, but check provider guidance).

### Proactive Rate Limit Management
Many clients track remaining capacity and queue requests before hitting the wall:

- Monitor `RateLimit-Remaining` headers
- If remaining capacity drops below a threshold, pause and wait
- Some providers publish expected rate limits at signup time, so you can implement queuing without waiting for 429s

**You should verify**: whether the provider publishes your limits upfront or only via headers, and whether preemptive backoff is recommended.

---

## What Varies by Provider (You Must Verify)

### Specific Questions to Answer for Your Provider
1. **Do they have multiple TPM limits?** (e.g., separate caps for input vs. output tokens)
2. **Is there a max tokens per request**, independent of TPM?
3. **How is concurrent request handling governed?** Some cap RPM but not concurrency; others do both.
4. **What headers do they send, and on which status codes?**
5. **Do they charge for failed requests** (429s or otherwise)?
6. **Is the rate limit per API key, per user account, or per organization?**
7. **Do they offer burstiness allowance?** (e.g., "you can exceed your TPM momentarily if the average stays under the limit")
8. **Do different endpoints have different limits?** (e.g., chat completions vs. embeddings)
9. **Is there a queuing service** (like OpenAI's Batch API) for non-real-time requests that bypasses rate limits?

---

## Confidence Breakdown

**I'm confident about:**
- The general categories (RPM, TPM, tiers, 429 responses, backoff strategy)
- That most modern providers use sliding windows for fairness
- That `Retry-After` is the most reliable signal across providers

**You'd want to double-check:**
- Exact numeric limits for your tier
- Which rate limit headers are actually returned (not all providers follow the standard closely)
- Whether limits are shared across models or per-model
- Charges for requests that fail due to rate limits
- Whether there's a bursty workload exception or special handling for batch operations

**Source it from**: each provider's official API docs (OpenAI, Anthropic, Google, etc. all publish this explicitly) and test with a small script using your API key.

---

### Next step
If you're building a rate limit handler, share which provider you're using and I can help you implement specific retry logic. Alternatively, link to their rate limit docs and I can flag what's unusual or easy to miss.