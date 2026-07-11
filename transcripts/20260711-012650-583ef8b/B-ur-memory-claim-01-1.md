**Operating from: Upper-Right (Build + Verify)**

### What I understand you're asking
You want an overview of how LLM API rate limiting typically works — the standard patterns across providers — with explicit markers showing what's industry-standard knowledge versus what needs provider-specific verification.

<assumptions>
  <task>You're building or debugging against an LLM API and want to understand the rate-limit landscape before diving into provider docs</task>
  <operator>You can verify provider-specific details yourself; you want the framework to know what to check</operator>
</assumptions>

---

## How LLM Rate Limits Typically Work

### Tier Structure
**[General knowledge]** Most LLM providers use tiered rate limits based on:
- **Account tier** (free, paid, enterprise) — determines your baseline limits
- **Usage-based progression** — some providers increase limits as you prove reliability
- **Request type** — chat completions, embeddings, fine-tuning sometimes have separate limits

Example tiers:
- Free: 3 requests/min, 90K tokens/day
- Pay-as-you-go: 3,500 requests/min, 90K tokens/min
- Enterprise: custom (negotiate with sales)

**[Verify for your provider]** Whether tiers are based on:
- Spend per month? Request count? Token count? A combination?
- Whether limits increase automatically or require a request to upgrade

---

### Rate-Limit Metrics
**[General knowledge]** Most providers enforce limits on *both* of these:
1. **Requests per minute (RPM)** — how many API calls you can make
2. **Tokens per minute (TPM)** — total tokens across all requests (input + output)

You'll hit whichever limit comes first. A single request can be small in RPM but huge in TPM if the prompt or completion is long.

**Example collision:**
- Your limit: 100 RPM, 90K TPM
- You fire 60 requests/min with 2K input tokens each
- You hit the TPM limit (120K tokens) before RPM (you're at 60 RPM)
- Further requests get rate-limited even though you're under 100 RPM

**[Verify for your provider]**
- Exact TPM and RPM limits for your tier
- Whether limits are per-account or per-API-key
- Whether batch processing (if offered) has different limits
- Whether there are separate limits for different model families

---

### Retry Headers
**[General knowledge]** When you hit a rate limit, the API returns HTTP 429 (Too Many Requests) with these standard headers:

| Header | What it tells you | Example |
|---|---|---|
| `Retry-After` | Seconds to wait before retrying | `Retry-After: 60` |
| `x-ratelimit-limit-requests` | Your RPM ceiling | `x-ratelimit-limit-requests: 3500` |
| `x-ratelimit-limit-tokens` | Your TPM ceiling | `x-ratelimit-limit-tokens: 90000` |
| `x-ratelimit-remaining-requests` | Requests left in current window | `x-ratelimit-remaining-requests: 2` |
| `x-ratelimit-remaining-tokens` | Tokens left in current window | `x-ratelimit-remaining-tokens: 45000` |
| `x-ratelimit-reset-requests` | Unix timestamp when RPM resets | `x-ratelimit-reset-requests: 1700000000` |
| `x-ratelimit-reset-tokens` | Unix timestamp when TPM resets | `x-ratelimit-reset-tokens: 1700000060` |

**Best practice:** Read these headers *before* hitting a limit. Use `remaining-requests` and `remaining-tokens` to preemptively back off rather than waiting for 429.

**[Verify for your provider]**
- Exact header names (some use `x-ratelimit-*`, others use different prefixes)
- Whether all headers are present or only some
- The time window (usually 1 minute, but some providers use different windows)
- Whether reset times are Unix timestamps or durations

---

### Reset Windows
**[General knowledge]** Most providers use **rolling 1-minute windows**. This means:
- At 12:00:00, you can make 100 requests
- At 12:00:30, you've made 50 → you can make 50 more before 12:01:00
- At 12:00:45, your first request at 12:00:00 expires → you can make 1 more
- At 12:01:00, your entire first minute bucket expires → full limit resets

This creates a "sliding window" effect, not a hard reset every minute.

**[Verify for your provider]**
- Window size (almost always 1 minute, but confirm)
- Whether it's a sliding window or fixed buckets
- Whether different metrics (RPM vs. TPM) reset at the same time

---

### Common Patterns for Handling Rate Limits

**[General knowledge — standard approaches]**

1. **Exponential backoff**: Wait `min(base * (2 ** attempt), max_wait)`, then retry
2. **Batch queueing**: Hold requests in a queue, release at a sustainable rate
3. **Preemptive throttling**: Monitor `remaining-requests` / `remaining-tokens`, pause before hitting the wall
4. **Concurrent request limiting**: Use semaphores to cap parallel requests

**[Verify for your provider]**
- Whether they explicitly recommend one approach over others
- Maximum sensible wait time (some providers have request timeouts at 60–120s)
- Whether batching (if available) bypasses standard rate limits

---

## What to Check for Your Specific Provider

Create a verification checklist before you code:

- [ ] RPM and TPM limits for your tier
- [ ] Whether limits are per-account or per-key
- [ ] Exact header names returned on 429
- [ ] Window size and whether it's sliding or fixed
- [ ] Whether they recommend a specific retry strategy
- [ ] Whether separate endpoints (embeddings, chat, fine-tuning) have separate limits
- [ ] Documentation link for their specific rate-limit behavior

**Provider docs often hide rate limits in:**
- "Limits" page (sometimes under Pricing)
- Rate limit error messages (test with a deliberately throttled call)
- API reference for the specific endpoint
- Rate limit increase request form (tells you what's tunable)

---

### What I'm confident about
- The general structure (tiers, RPM/TPM, 429 responses, headers) is consistent across major LLM providers
- Reset windows are almost always 1 minute, rolling

### What I'd double-check
- Exact header names and which ones are guaranteed vs. optional (varies between OpenAI, Anthropic, Azure, etc.)
- Whether some providers count input/output tokens separately in the TPM calculation (most don't, but a few do)
- Enterprise/custom tiers often have completely different mechanics — if that's your case, the above may not apply