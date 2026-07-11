# Debugging Intermittent 502s

Start with these high-value steps in parallel:

## 1. **Correlate with your logs** (do this first)
- Pull 502 error timestamps
- Cross-reference against:
  - Application error logs (exceptions, timeouts, crashes)
  - Infrastructure metrics (CPU, memory, disk spikes)
  - Network/load balancer logs
  - Database slow query logs, connection pool exhaustion
  - Third-party service calls that might timeout

The 502 is just the symptom—the cause is usually upstream.

## 2. **Check resource limits**
```
At 502 time:
- Is any process hitting memory ceiling?
- Swap usage spiking?
- File descriptor limits?
- Database connection pool saturated?
- Thread pool exhausted?
```
These are sneaky because they don't *feel* like problems until they break.

## 3. **Review recent changes**
- Code deploys (even small ones)
- Dependency updates
- Infrastructure changes
- Traffic pattern shifts
- Third-party API changes

If it started recently, that's your answer.

## 4. **Request-level patterns**
- Are 502s clustered to specific endpoints?
- Specific request types (large payloads, specific headers)?
- Requests to slow downstream services?
- Requests that trigger cache misses?

## 5. **Quick wins to try**
- Increase application timeout values (might be timing out waiting for something)
- Increase load balancer timeout
- Add more worker processes/threads
- Restart application (tells you if it's a gradual resource leak)

**What to capture next time it happens:**
- Exact timestamp
- All logs within ±30 seconds
- Metrics snapshot (everything available)
- Sample of requests around that time

If logs are sparse, enable debug logging temporarily—one hour of verbose logs is worth finding this.

What does your stack look like? (Language, load balancer, any workers/queues?)