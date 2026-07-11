**Operating from: Upper-Right (Build + Verify)**

### Confirming before I proceed

I'm treating this as a request for general knowledge about LLM rate-limiting patterns, with verification boundaries clearly marked. I assume you want a mental model you can apply to any provider's docs, not provider-specific numbers.

---

## How API Rate Limits Work: General Patterns

### Tier Structure

**General knowledge** — all major LLM providers (OpenAI, Anthropic, Google, AWS Bedrock, etc.) use similar tier models:

- **Free tier**: lowest limits, often per-minute or per-day caps, sometimes per-account rather than per-request
- **Pay-as-you-go**: higher per-minute limits, often with soft caps that trigger throttling
- **Enterprise/dedicated**: negotiated limits, sometimes unlimited within SLA guarantees

Tiers typically correlate with billing level, account age, and usage history. New accounts are frequently rate-limited more aggressively than established ones.

### Rate Limit Units

**General knowledge** — two primary units:

1. **Requests per minute (RPM)**: count of API calls, regardless of size
2. **Tokens per minute (TPM)**: cumulative token count (prompt + completion). This is the more common *effective* limit.

Example: if your TPM limit is 90,000 and you send a request with 1,000 prompt tokens expecting 2,000 completion tokens, that consumes 3,000 of your budget.

Some providers also have **concurrent request limits** (how many parallel requests you can have in flight at once).

---

### HTTP Response Headers (Retry Headers)

**General knowledge** — standardized header pattern across providers:

| Header | Meaning | Example |
|--------|---------|---------|
| `x-ratelimit-limit-requests` | Total RPM allowed | `3500` |
| `x-ratelimit-limit-tokens` | Total TPM allowed | `90000` |
| `x-ratelimit-remaining-requests` | RPM left in current window | `2847` |
| `x-ratelimit-remaining-tokens` | TPM left in current window | `87234` |
| `x-ratelimit-reset-requests` | Seconds until RPM counter resets | `45` |
| `x-ratelimit-reset-tokens` | Seconds until TPM counter resets | `23` |
| `Retry-After` | Seconds to wait before retrying (on 429 response) | `60` |

**What to verify**: header names vary by provider. OpenAI uses the `x-ratelimit-*` pattern. Google Vertex AI uses `x-goog-ratelimit-info`. AWS Bedrock has different naming entirely. Check your provider's docs for the exact header names they emit.

---

### Rate Limit Windows

**General knowledge** — limits reset on a rolling or fixed window:

- **Rolling window** (most common): the limit applies to a sliding 60-second window. As soon as a request leaves the window, its tokens "free up."
- **Fixed window**: limits reset at fixed times (e.g., midnight UTC). Less flexible but easier to predict.

Most providers use rolling windows for per-minute limits.

**What to verify**: confirm whether your provider uses rolling or fixed, and what the window size actually is (it's usually 60 seconds, but not always).

---

### Handling 429 (Rate Limited) Responses

**General knowledge** — standard retry pattern:

1. Provider returns HTTP 429 with `Retry-After` header
2. Client waits the specified seconds (or uses exponential backoff if no header)
3. Retry the request

Most robust clients implement:
- **Exponential backoff**: wait 1s, then 2s, then 4s, capping at some max (e.g., 60s)
- **Jitter**: add random noise to prevent thundering herd (all clients retrying at the same time)
- **Max retries**: give up after N attempts to avoid infinite loops

Example backoff: `wait_time = min(2^attempt + random(0, 2^attempt), 60)`

**What to verify**: whether the provider honors `Retry-After` and what its value represents (seconds? milliseconds?). Some providers don't emit it and expect you to guess or check remaining headers instead.

---

### Token Counting

**General knowledge** — tokens consumed depend on the model and text:

- English text ≈ 1 token per 4 characters (rough heuristic)
- Most providers count prompt tokens separately from completion tokens, both against your TPM limit
- Some models have different token costs for input vs. output (e.g., Claude 3.5 Sonnet costs less per input token than output)

**What to verify for your provider**:
- Whether input and output tokens are counted equally or have different weights
- Whether system prompts are counted separately or bundled with your prompt
- Whether there's a tokenizer SDK or API you should use to pre-calculate costs
- Whether tool/function definitions consume tokens (they usually do)

---

### Queuing and Backpressure Patterns

**General knowledge** — when you hit rate limits, common strategies are:

1. **Immediate retry with backoff** — simple, works for temporary spikes
2. **Token bucket queue** — maintain a local queue, feed requests to the API at a rate you know won't exceed limits
3. **Adaptive throttling** — monitor remaining headers and slow down proactively before hitting 429

Adaptive throttling is most robust: if `x-ratelimit-remaining-tokens` drops below 20% of your limit, pause new requests until it recovers.

**What to verify**: whether your provider allows or recommends any of these strategies in their docs. Some have guidance on optimal request batching.

---

## Summary Table: What to Look Up for Your Specific Provider

| Element | General Principle | Where to Verify |
|---------|-------------------|-----------------|
| Tier structure | Tiers correlate with billing level | Provider pricing page |
| Rate limit units | RPM and/or TPM | API docs, rate limit section |
| Response headers | `x-ratelimit-*` pattern is common but not universal | API reference (response headers section) |
| Window type | Usually rolling 60 seconds | Rate limit docs or support |
| Retry header | `Retry-After` is standard but not guaranteed | API docs, error handling section |
| Token counting | Varies by model, sometimes input ≠ output | Model documentation, tokenizer SDK page |
| Header names | Names vary significantly | Provider's API reference |

---

## What I'm Confident About
- The general tier structure (free → pay-as-you-go → enterprise) is universal
- TPM is the effective bottleneck for most workloads
- Rolling windows and exponential backoff are industry standards
- Token-counting logic is provider-specific and needs verification

## What I'd Double-Check
- **Exact header names**: these are not standardized and vary by provider
- **Token weighting**: some models charge differently for input vs. output tokens; this significantly affects real-world TPM planning
- **System prompt token accounting**: some providers count it, some don't, and it affects your effective limit
- **Retry-After semantics**: check whether your provider even emits this header, and whether it's in seconds or milliseconds