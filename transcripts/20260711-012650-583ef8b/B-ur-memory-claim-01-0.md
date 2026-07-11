**Operating from: Upper-Right (Build + Verify)**

### Confirming before I proceed

I'm treating this as a request for general knowledge about LLM rate-limiting patterns, with clear boundaries between what's universally true and what varies by provider. I'm assuming you want this as reference material for understanding how to design client logic, not as a source of truth for any specific provider's current limits.

---

## How LLM Rate Limits Typically Work

### Tier Structure

**General pattern** (applies to OpenAI, Anthropic, AWS Bedrock, Google Vertex, and most major providers):
- **Free tier**: lowest limits, often enforced aggressively. Typical: 3–20 requests per minute, 90k–150k tokens per day.
- **Pay-as-you-go**: higher limits, sometimes with soft caps. Typical: 3,500–90,000 tokens per minute depending on model and account age.
- **Dedicated/enterprise**: custom limits, often negotiated per contract.

Tier placement depends on:
- Account age and usage history (newer accounts start lower)
- Payment method validation (credit card vs. billing account)
- Explicit tier selection (choosing "pro" vs. "basic")
- Total spend or committed spend level

### Token Budgets

**General approach**:
- Limits are expressed as **tokens per minute (TPM)** for input + output combined, or sometimes separated.
- Some providers also enforce **requests per minute (RPM)** as a secondary limit (e.g., "3,500 TPM *and* 90 RPM").
- The token count includes both prompt and completion tokens; some providers count them equally, others weight output tokens higher.

**Typical ranges** (as of late 2024, varies by model):
- GPT-4 (OpenAI): 40k–200k TPM at scale
- Claude 3 (Anthropic): 100k TPM standard, 200k–600k with provisioned throughput
- Gemini (Google): 60 requests/min free, higher tiers scale by committed spend

**You should verify**: Your specific provider publishes current limits in their pricing or quota documentation. These change frequently and vary by model.

### Retry Headers

**Standard HTTP headers** (RFC 7231 + provider custom conventions):

| Header | Set by | Typical value | What it means |
|---|---|---|---|
| `Retry-After` | Provider | `60` or `2024-01-15T12:34:56Z` | Wait this many seconds or until this time before retrying |
| `x-ratelimit-limit-requests` | Provider | `3500` | Your quota for requests per minute |
| `x-ratelimit-limit-tokens` | Provider | `90000` | Your quota for tokens per minute |
| `x-ratelimit-remaining-requests` | Provider | `3499` | Requests left in current window |
| `x-ratelimit-remaining-tokens` | Provider | `87234` | Tokens left in current window |
| `x-ratelimit-reset-requests` | Provider | `2024-01-15T12:34:56Z` | When your request quota resets |
| `x-ratelimit-reset-tokens` | Provider | `2024-01-15T12:34:56Z` | When your token quota resets |

**General behavior**:
- A `429 Too Many Requests` response includes `Retry-After` in the headers.
- Remaining-* headers are returned on *successful* (2xx) responses so you can track your budget in real time.
- Reset times are absolute (wall-clock), not relative to request time.

**You should verify**: Header names vary. OpenAI uses `x-ratelimit-*`, Anthropic uses the same, but Google and AWS may use different conventions (e.g., `RateLimit-Remaining-Requests` vs. `x-ratelimit-remaining-requests`). Check your provider's API docs.

### Windowing

**General pattern** (rolling minute):
- Most providers use a **rolling 60-second window**, not a fixed calendar minute.
- If you send 100 requests at second 0, you can send another 100 at second 60.01, not at second 61.00.
- Some providers apply **per-second smoothing** as well (maximum burst per second), to prevent DoS-like traffic patterns.

**You should verify**: Whether your provider uses rolling windows or calendar windows, and whether they enforce per-second limits.

### Practical Retry Logic

**General recommended approach**:
1. Parse `Retry-After` header (prefer it over guessing).
2. If `Retry-After` is absent, use exponential backoff with jitter: `wait = min(max_wait, 2^attempt + random(0, 1))`.
3. Track remaining tokens/requests from response headers; stop before hitting zero (don't rely on 429s as your only safety valve).
4. For batch jobs, pace requests to stay well below the limit (e.g., 80% of capacity) to avoid rate-limit surprises.

---

## What to Verify for Your Specific Provider

Before building retry logic, check these documents:

- **Rate limit tiers and current numbers** (pricing or quota page)
- **Which headers are returned** (API reference)
- **Whether limits are per-token or per-request** or both
- **Reset behavior**: rolling vs. calendar window
- **Per-second burst limits** (if applicable)
- **Soft vs. hard limits**: can you exceed briefly, or does it fail immediately?
- **Free-tier enforcement** (sometimes stricter than paid tiers)

Most providers update these regularly; pull from their official docs, not guides or blog posts.