**Operating from: Upper-Right (Build + Verify)**

### What I understand you're asking
A general explanation of how LLM API rate limiting works—the common patterns across providers—with clear callouts for what varies by provider and needs verification.

<assumptions>
  <project>You're building or integrating with an LLM API and need to understand rate limit mechanics before diving into a specific provider's docs.</project>
  <task>You want a mental model of the space so you can recognize what's standard, what's provider-specific, and what to look for when you do check the docs.</task>
  <operator>You're technically capable but want clarity on where to trust this overview and where to verify.</operator>
</assumptions>

---

## How Rate Limits Typically Work

### Tier Structure
**General knowledge** ✓
- Providers usually offer multiple tier levels (free, pro, enterprise) with different rate limits.
- Within a tier, limits are often specified in two dimensions: **requests per minute** (RPM) and **tokens per minute** (TPM).
- Higher tiers unlock higher ceilings and sometimes priority queuing.

**Verify for your provider:**
- Exact tier names and boundaries (OpenAI calls them "Free," "Pay-as-you-go," "Usage Tier N"; others differ)
- Whether TPM or RPM is the tighter constraint for your use case
- Whether limits apply globally or per-organization/per-API-key

### Rate Limit Headers
**General knowledge** ✓
- Providers return HTTP headers on *every* response indicating remaining quota and reset times.
- Common header names: `x-ratelimit-limit-requests`, `x-ratelimit-remaining-requests`, `x-ratelimit-reset-requests`, and token equivalents.
- These let you implement client-side backoff *before* hitting the wall.

**Verify for your provider:**
- Exact header names (naming varies slightly)
- Whether they return both RPM and TPM headers, or just one
- The time format for reset headers (Unix epoch, ISO 8601, seconds-until-reset)
- Whether the headers distinguish between different quota pools (e.g., tier limit vs. org limit)

### Hitting the Limit
**General knowledge** ✓
- When you exceed a limit, the API returns HTTP 429 (Too Many Requests).
- The 429 response typically includes a `Retry-After` header indicating how long to wait before retrying.
- Exponential backoff is standard practice: wait 2s, then 4s, then 8s, etc., with optional jitter to avoid thundering herds.

**Verify for your provider:**
- Whether `Retry-After` is in seconds or milliseconds
- Whether it's absolute or relative (some APIs return a timestamp; others return a duration)
- Any guidance on maximum retry attempts or total time to give up
- Whether different endpoints have different limits (sometimes embedding or fine-tuning has its own pool)

### Soft vs. Hard Limits
**General knowledge** ✓
- Some providers allow brief bursts *above* the stated TPM, then throttle back.
- Others enforce hard boundaries—you're rejected immediately if you exceed the second-by-second allocation.
- Burst allowance is often 2–3× the per-second rate but is rate-limited back down over the minute.

**Verify for your provider:**
- Whether they publish burst behavior at all (some don't)
- The grace period, if any, for exceeding limits
- Whether it applies uniformly across all tiers

---

## What Changes by Provider

| Aspect | What to Check |
|--------|---------------|
| **Granularity** | Do they limit per API key? Per org? Per user? Per IP? |
| **Rate limit pools** | Do different endpoint types (chat, embedding, moderation) share a pool or have separate limits? |
| **Upgrade rules** | Can you request a higher limit, or is it automatic based on spend? |
| **Concurrency** | Do they limit simultaneous connections, or only aggregate throughput? |
| **Batch processing** | Do batch APIs have different (usually higher) limits? |

---

## How to Verify for Your Specific Provider

1. **API docs → Rate Limits section**: Usually has a table with exact numbers and header names.
2. **SDK/client library**: Check if it has built-in rate-limit handling. The code often reveals nuances the docs don't.
3. **Error responses**: Make a test request that fails intentionally and inspect the headers and body.
4. **Support or community**: If docs are vague, ask—this is a common question.

**Marked as confident** ✓: the general structure above (tiers, headers, 429 response, backoff pattern) is standard across all major providers.

**Marked as provider-specific** ⚠: everything in the "Verify for your provider" sections—the details matter for implementation.