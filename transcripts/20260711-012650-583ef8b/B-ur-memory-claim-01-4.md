**Operating from: Upper-Right (Build + Verify)**

### Confirming before I proceed

I'm treating this as a general educational summary about LLM rate-limiting patterns, not a guide to a specific provider's current implementation. I'm assuming you want to understand the mechanics so you can read a provider's docs intelligently, not that you need exact numbers for production use.

---

## How LLM API Rate Limits Work

### Tier Structure

**General pattern** (confirmed across OpenAI, Anthropic, Google, AWS):
- **Free/trial tier**: lowest limits, often request-per-minute (RPM) only
- **Pay-as-you-go**: higher limits, usually both RPM and tokens-per-minute (TPM)
- **Enterprise**: custom limits, negotiated per contract

Tiers typically scale with:
- Your cumulative spend (historical or current month)
- Explicit tier selection at signup
- Account age or verification status

**What to verify for your provider**: Exact tier names, the triggers for automatic upgrade, and whether there's a way to request higher limits without waiting for spend to accumulate.

---

### Rate Limit Dimensions

LLM providers typically enforce **two independent limits**:

| Dimension | What it measures | Why it matters | Typical format |
|-----------|------------------|---|---|
| **Requests per minute (RPM)** | Number of API calls | Prevents connection flooding; cheaper to enforce | "100 RPM" |
| **Tokens per minute (TPM)** | Input + output tokens | Prevents compute exhaustion; the real bottleneck | "40,000 TPM" |

Both must be satisfied simultaneously. You can hit TPM before RPM, or vice versa.

**Example**: At 100 RPM with 40,000 TPM, if your avg request is 500 tokens (input + output), you're limited by RPM (100 requests × 500 tokens = 50k tokens, which exceeds 40k TPM). If avg request is 100 tokens, you're limited by TPM.

**What to verify**: Your provider's exact limits for your tier, and whether they're enforced per-minute or per-second (the rollover window matters for burst handling).

---

### Retry Headers (HTTP 429 and Related)

When you hit a rate limit, the API returns **HTTP 429 (Too Many Requests)** with headers that tell you how to back off:

**Standard headers** (nearly universal):
- `Retry-After`: seconds to wait before retrying (integer or HTTP date)
- `RateLimit-Limit-Requests`: your RPM limit
- `RateLimit-Limit-Tokens`: your TPM limit
- `RateLimit-Remaining-Requests`: how many requests left in current window
- `RateLimit-Remaining-Tokens`: how many tokens left in current window

**Less common but useful** (varies by provider):
- `RateLimit-Reset-Requests`: Unix timestamp when RPM resets
- `RateLimit-Reset-Tokens`: Unix timestamp when TPM resets

**Correct behavior** (general best practice):
1. Read `Retry-After` from the 429 response
2. Wait that duration (at minimum)
3. Retry the request
4. Use exponential backoff if retries fail again (this is defensive; a single `Retry-After` should be sufficient if honored)

**What to verify**: The exact header names your provider uses. Some use `retry-after` (lowercase), some use `X-RateLimit-*` prefixes, some omit headers entirely and rely on documentation. Check your provider's docs for the precise names and whether they're always present.

---

### Burst Handling and Token Bucketing

**General mechanism**: Rate limits are enforced on a rolling window, usually per minute:
- Tokens consumed in the last 60 seconds count against your TPM limit
- Once a second rolls out of the window, its tokens become available again
- This means you can have brief spikes above your average rate, but not sustained ones

**What to verify**: Whether your provider uses a strict per-minute window, a sliding window, or a token-bucket algorithm (smoother burst absorption). This affects how you should batch requests.

---

### Quota vs. Rate Limit

**Don't confuse these** (common source of confusion):

| | Rate Limit | Quota |
|---|---|---|
| **What** | Throughput cap per unit time | Total usage cap per billing period |
| **Error** | HTTP 429 | Usually billing-side, not an API error |
| **Recovery** | Wait and retry | Wait until next billing cycle or add payment method |

Rate limits reset on a per-minute basis. Quotas reset monthly (or on your billing cycle).

**What to verify**: Your provider's quota model — daily, monthly, per-token-purchased, etc.

---

### Common Gotchas

**General knowledge** (applies broadly):
1. **Streaming requests count against limits too.** The entire response token count is charged immediately or as tokens are generated, depending on the provider.
2. **Retry-After is a minimum, not an exact target.** Waiting slightly longer is safe; retrying before it expires will fail.
3. **Limits apply per API key**, not per user or per account (unless explicitly documented otherwise).
4. **Batch endpoints often have separate limits** — much higher TPM, but async.

**What to verify**: How your specific provider charges streaming tokens, whether they offer batch/async APIs with higher limits, and whether limits are per-key or per-account.

---

## Summary for Implementation

**You should verify with your provider:**
- [ ] Exact TPM and RPM limits for your tier
- [ ] The specific header names used in 429 responses
- [ ] Whether limits reset per-minute, per-second, or use token-bucket
- [ ] How they charge streaming tokens (upfront vs. as-streamed)
- [ ] Whether they offer batch/async APIs with separate limits
- [ ] Their official guidance on retry strategy (most say: read Retry-After and use it, period)

**You can rely on as general knowledge:**
- The two-axis model (RPM + TPM)
- Tier structure (free → paid → enterprise)
- HTTP 429 as the signal
- Exponential backoff as a defensive measure
- Quota vs. rate limit distinction

---

**Next step**: Grab your provider's rate-limit documentation (usually under "Limits" or "Quotas") and cross-reference it against this framework. The names will vary, but the structure should map cleanly.