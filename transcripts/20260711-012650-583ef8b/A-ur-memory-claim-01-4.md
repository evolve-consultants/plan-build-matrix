# LLM API Rate Limiting: General Patterns

## Common Tier Structure (General Knowledge)

Most major LLM providers use similar frameworks:

**Typical Tier Progression:**
- Free/Trial tier: Very restrictive (e.g., 3-5 requests/minute)
- Pay-as-you-go: Moderate limits that scale with spending
- Pro/Business tiers: Higher throughput, sometimes unlimited
- Enterprise: Custom negotiated limits

**Metrics Used:**
- **Requests per minute (RPM)** — how many API calls
- **Tokens per minute (TPM)** — the primary bottleneck for LLMs
- Sometimes **concurrent requests** limits

## How Token Limits Work (General Knowledge)

```
TPM limit applies across:
- Input tokens (prompt)
- Output tokens (completion)
- Both counted toward the same limit per minute

Example: 90K TPM tier
- Could be: 60K input + 30K output tokens
- Or: any mix totaling 90K
```

The minute "window" typically resets on a rolling basis (not calendar minutes).

## Rate Limit Response Headers (General Knowledge)

Standard HTTP response headers you'll encounter:

| Header | Meaning | Typical Value |
|--------|---------|---|
| `x-ratelimit-limit-requests` | RPM ceiling | `3000` |
| `x-ratelimit-limit-tokens` | TPM ceiling | `90000` |
| `x-ratelimit-remaining-requests` | RPM left this window | `2995` |
| `x-ratelimit-remaining-tokens` | TPM left this window | `87543` |
| `retry-after` | Seconds to wait before retrying | `15` |

**⚠️ VERIFY FOR YOUR PROVIDER:** Header names vary significantly. Some use `ratelimit-`, others use `x-rate-limit-`, some use entirely custom headers.

## Retry Logic (General Knowledge)

Standard exponential backoff pattern:

```python
import time

attempt = 0
max_attempts = 5
base_delay = 1

while attempt < max_attempts:
    try:
        response = api_call()
        return response
    except RateLimitError as e:
        attempt += 1
        # Use retry-after header if provided
        wait_time = int(e.headers.get('retry-after', base_delay * (2 ** attempt)))
        print(f"Rate limited. Waiting {wait_time}s...")
        time.sleep(wait_time)
    except Exception as e:
        raise
```

**⚠️ VERIFY:** Check if your provider recommends specific backoff strategies. Some have penalties for aggressive retrying.

---

## Provider-Specific Things to Verify

Before implementing, **always check your provider's actual documentation:**

### OpenAI
- [ ] Do TPM limits vary by model? (they do)
- [ ] What's the actual header format they use?
- [ ] Do usage tiers reset monthly or rolling?

### Anthropic
- [ ] What's their batching API rate limit vs regular?
- [ ] Token counting methodology (how do they count?)

### Google/Vertex AI
- [ ] Regional rate limits?
- [ ] Do quotas work differently across regions?

### Azure OpenAI
- [ ] Deployment-specific limits?
- [ ] How does throttling interact with reserved capacity?

### Any Provider
- [ ] **Do they offer burst capacity?** (some allow brief overages)
- [ ] **What counts toward limits?** (do retries count twice?)
- [ ] **Quota vs rate limit** — some providers distinguish these
- [ ] **Soft vs hard limits** — what happens at the boundary?

---

## Red Flags in Rate Limit Responses

These suggest you should check documentation:

- **Missing rate-limit headers** entirely — provider may use polling
- **Inconsistent remaining counts** — may indicate batched processing
- **429 responses without retry-after** — check docs for their strategy
- **Different limits per endpoint** — verify the matrix by model/endpoint

## Quick Implementation Checklist

```
Before going to production:
☐ Read provider's rate limiting section (not optional)
☐ Test hitting the limit in sandbox/dev tier
☐ Verify actual header names they use
☐ Confirm TPM counting includes input+output
☐ Check if limits differ by model
☐ Implement retry-after parsing from their format
☐ Load test briefly to confirm behavior
☐ Set up monitoring for rate limit headers
```

The general patterns are consistent, but implementation details vary enough that skipping provider docs creates unnecessary debugging later.