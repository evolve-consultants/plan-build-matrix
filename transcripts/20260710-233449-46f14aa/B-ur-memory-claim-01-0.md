**Trivial — matrix not applied.** Classified this as a factual summary with no downstream dependencies on specific implementation choices. You own verification against any provider's actual docs.

---

## General Knowledge: How LLM API Rate Limits Work

### Tier Structure
Most providers (OpenAI, Anthropic, AWS Bedrock, etc.) organize limits by subscription tier:
- **Free/trial tier**: lowest limits, often per-minute caps on requests
- **Pay-as-you-go**: higher limits, sometimes with soft caps that trigger billing warnings
- **Enterprise**: custom negotiated limits, often per-second or burst-based

Limits are typically **per account** or **per API key**, not per user—you control subdivision if needed.

### Token-Based Rate Limits
The standard modern approach:
- Limit is expressed as **tokens per minute (TPM)** or **requests per minute (RPM)**
- Both input and output tokens count against the limit (though some providers weight them differently)
- Exceeding the limit returns a `429 Too Many Requests` response
- **No automatic queuing**: the request fails immediately; retry is your responsibility

Example: "GPT-4 on pay-as-you-go: 90,000 TPM" means 90k tokens (prompt + completion) per rolling minute.

### Retry Headers
When rate-limited, the response includes:
- **`Retry-After`** (HTTP standard): seconds to wait before retrying
  - Value can be a number (seconds) or an HTTP date
  - Some providers return this; others don't
- **`x-ratelimit-reset-tokens`** or **`x-ratelimit-reset-requests`** (provider-specific): timestamp when the limit resets
- **`x-ratelimit-remaining-tokens`** or **`x-ratelimit-limit-tokens`** (provider-specific): tokens remaining in current window

Standard practice:
1. Check `Retry-After` if present; if not, exponential backoff (1s, 2s, 4s, etc.)
2. Log the reset time so you don't retry before the window actually clears
3. Handle `429` as retriable; handle `401` or `400` as terminal

### Burst vs. Sustained Limits
Some providers distinguish:
- **Concurrent requests**: how many requests can be in-flight at once
- **Throughput**: tokens per minute averaged over time
- **Burst**: short-term spikes allowed above sustained rate

This matters for batching logic—you might hit a per-second limit even if your TPM is fine.

---

## What You Should Verify for Your Specific Provider

- [ ] What tier are you on, and what are the exact TPM/RPM numbers?
- [ ] Are input and output tokens weighted equally, or does the provider count only output?
- [ ] Does the provider return `Retry-After` headers, or do you need to implement your own backoff?
- [ ] What headers do they use for rate-limit info (`x-ratelimit-*`, `RateLimit-*`, something else)?
- [ ] Is there a distinction between per-second and per-minute limits, or burst allowance?
- [ ] Can you request a limit increase, and what's the process?
- [ ] Do they offer batch APIs (asynchronous, higher limits) as an alternative?

Check the provider's rate-limit documentation directly—naming conventions and behavior vary enough that assuming one provider's pattern applies to another often breaks.