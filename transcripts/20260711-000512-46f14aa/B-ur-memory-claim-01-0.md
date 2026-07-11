**Operating from: Upper-Right (Build + Verify)**

### What I understand you're asking
You want a general explainer of how LLM API rate limiting typically works — tiers, tokens/minute (TPM), requests/minute (RPM), retry headers — with clear separation between what's broadly true across providers and what varies enough that you'd need to check provider docs directly.

<assumptions>
<project>No specific provider or codebase mentioned — this is a conceptual/reference request, not tied to a particular integration yet.</project>
<task>You're likely either designing a client that needs to handle rate limits gracefully, or evaluating providers, and want a mental model before diving into provider-specific docs.</task>
<operator>You have basic familiarity with HTTP APIs (status codes, headers) and don't need those fundamentals explained.</operator>
</assumptions>

### The artifact

**Tiers**
Most providers gate rate limits behind account tiers, usually based on cumulative spend, account age, or manual approval (e.g., "free," "tier 1," "tier 5," "enterprise"). Higher tiers unlock higher TPM/RPM ceilings and sometimes priority queuing. `<!-- verify: exact tier thresholds and what triggers upgrades — this varies a lot and changes over time -->`

**The two core limit dimensions**
- **RPM (requests per minute)**: caps how many API calls you can make regardless of size.
- **TPM (tokens per minute)**: caps total tokens (input + output, sometimes counted differently) processed per minute.
Both usually apply simultaneously — you can hit whichever ceiling comes first. Some providers also cap RPD (requests per day) or concurrent requests. `<!-- verify: which dimensions a specific provider enforces, and whether input/output tokens count separately or combined -->`

**Scope of limits**
Limits are typically per API key or per organization/account, sometimes per model (a GPT-4-class model may have a much lower TPM than a smaller model). `<!-- verify: whether limits are per-key, per-org, or per-model for your provider -->`

**How you find out you're limited**
Standard pattern: HTTP `429 Too Many Requests` response. Providers commonly include headers indicating remaining quota and reset time, e.g.:
```
x-ratelimit-limit-requests
x-ratelimit-remaining-requests
x-ratelimit-limit-tokens
x-ratelimit-remaining-tokens
retry-after
```
The exact header names and casing differ by provider — the pattern (limit/remaining/reset per dimension) is common; the naming is not standardized. `<!-- verify: exact header names for your provider — this is the single most likely detail to be wrong if assumed generically -->`

**Retry behavior**
General best practice, used across most SDKs: exponential backoff with jitter, respecting `retry-after` if present, capped at some max retry count. Some providers document a recommended backoff strategy or offer this via an official SDK. `<!-- verify: whether the provider's SDK already implements backoff for you — often it does, and hand-rolling it is redundant -->`

### What I'm confident about
- The RPM/TPM dual-limit model and tier-gating pattern are near-universal across major LLM providers.
- 429 status code + some form of retry-after signaling is the standard mechanism.
- Exponential backoff with jitter is the standard client-side response.

### What I'd double-check
- Exact header names/casing for your target provider (highest variance, easy to get wrong).
- Whether TPM counts input tokens, output tokens, or both.
- Whether limits are per-key, per-org, or per-model — this affects how you architect concurrent usage.
- Tier thresholds and how to request increases — these change frequently and aren't stable enough to treat as general knowledge.

*If you tell me the specific provider, I can move to Bottom-Right and give you the concrete numbers/headers instead of the general pattern.*