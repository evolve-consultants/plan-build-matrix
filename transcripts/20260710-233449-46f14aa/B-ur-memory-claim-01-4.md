**Operating from: Upper-Right (Build + Verify)**

### Confirming before I proceed

I'm treating this as a request for general LLM rate-limiting patterns with clear separation of universal conventions from provider-specific details. I'll flag what's industry-standard versus what needs verification per provider.

### The artifact

## How LLM API Rate Limits Typically Work

### **Tier Structure** (general knowledge — but verify specifics per provider)

Most LLM providers offer rate limits tied to **pricing tiers**:

- **Free/Trial tier**: lowest TPM (tokens per minute), often 90k–350k TPM depending on provider
- **Pay-as-you-go**: higher TPM, sometimes with request-per-minute (RPM) limits as a secondary constraint
- **Dedicated/Enterprise**: negotiated limits or removed limits entirely

The tier you're on determines your **hard ceiling**. Exceeding it returns a 429 (Too Many Requests) or similar error.

### **Rate Limit Dimensions** (general knowledge)

Providers typically enforce **at least one** of these:

| Dimension | Unit | Meaning | Example |
|-----------|------|---------|---------|
| **TPM** | tokens/minute | Total tokens (input + output) in a rolling 60-second window | OpenAI: 90k TPM on free tier |
| **RPM** | requests/minute | Number of API calls in a rolling 60-second window | Often 3–60 RPM depending on tier |
| **Concurrent requests** | parallel calls | Number of simultaneous in-flight requests | Less common; some providers enforce this |

**What to verify**: Which dimensions your target provider enforces and how they interact (do both TPM *and* RPM apply, or just one?).

### **Retry Headers** (industry-standard pattern — verify exact header names)

When you hit a rate limit, the provider returns a **429 response** with these headers (names may vary slightly):

| Header | Meaning | Example | Verify: |
|--------|---------|---------|---------|
| `Retry-After` | Seconds to wait before retrying | `60` | Standard HTTP; all major providers use this |
| `x-ratelimit-limit-tokens` | Your TPM ceiling | `90000` | OpenAI convention; name varies by provider |
| `x-ratelimit-remaining-tokens` | Tokens left in current window | `45000` | Lets you preemptively back off before hitting limit |
| `x-ratelimit-reset-tokens` | Unix timestamp when quota resets | `1699564800` | Helps calculate wait time |

**What to verify**: Exact header names for your provider (some use `X-RateLimit-*`, some use `x-ratelimit-*`, some use custom names like `Anthropic-Rate-Limit-*`).

### **Practical Retry Logic** (general knowledge)

Standard pattern:

```
1. Make request
2. If 429 received:
   a. Read Retry-After header (or calculate from reset timestamp)
   b. Wait that duration
   c. Retry (usually 3–5 times max)
3. If still failing after max retries, surface error to user
```

**Exponential backoff** is common for transient errors, but for rate limits, the provider tells you exactly when to retry — follow that guidance.

### **What changes per provider** (requires verification)

- **Token counting**: How input vs. output tokens are counted toward TPM (some charge differently for cached tokens, tools, system prompts)
- **Window type**: Sliding window (most common) vs. fixed buckets
- **Reset behavior**: Whether unused quota carries over or resets on schedule
- **Burst allowance**: Whether you can exceed TPM briefly if you have unused quota (OpenAI allows this; others don't)
- **Organization/project limits**: Whether you have sub-limits below your tier limit
- **Free trial restrictions**: Whether free tier has additional per-day or per-month caps

---

### What I'm confident about

- Rate limits are enforced at the provider level, not per API key (one tier = one limit across all keys in it)
- 429 responses with retry headers are the standard across major providers
- TPM is the most common bottleneck; RPM is secondary and often generous
- Retry-After is always present and should always be respected

### What I'd double-check

- **Exact rate limit values for your tier** — these change frequently and vary by model and region
- **Header names in your provider's documentation** — they're usually X-RateLimit-* or x-ratelimit-*, but some providers use custom names
- **Whether token counting includes system prompts/tools** — this affects how quickly you hit limits in practice
- **Burst behavior** — whether unused quota rolls over minute-to-minute or if you're strictly capped per window
- **Whether you have org-level vs. project-level limits** — some providers enforce both, and the stricter one wins

### Where to find this

Check your provider's rate-limiting documentation directly; it's usually in a single well-labeled section. Look for: tier definitions, TPM/RPM values, retry header reference, and any gotchas specific to your model or use case.