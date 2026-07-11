**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You have a production API that occasionally returns 502 Bad Gateway errors (~1/hour) with no obvious trigger pattern, and you need a systematic way to start investigating rather than guessing at root causes.

<assumptions>
  <project>
    - You have standard observability (logs, metrics, maybe traces)
    - The API is multi-instance (load-balanced) or uses external services
    - 502s are intermittent enough that you can't reproduce on demand
    - You've already ruled out "obvious" things like out-of-disk or OOM
  </project>
  <task>
    - You want a diagnostic framework — the right questions to ask and the order to ask them
    - You're looking for where to point your team's effort first, not a full runbook
  </task>
  <operator>
    - You have access to logs, metrics, and probably can deploy observability changes
    - You own the API code but maybe not the full stack (load balancer, reverse proxy, databases)
  </operator>
</assumptions>

### What I'm unsure of
- **Stack shape**: Is this a single service, microservices, or calling external APIs? (Changes whether to investigate internal state vs. downstream dependencies first.)
- **Observability ceiling**: Do you have distributed traces, or just logs and metrics? (Affects how much visibility you can get without code changes.)
- **"No pattern" specificity**: Have you checked time-of-day, request volume, request *type*, or specific endpoints? Or is it truly random across all traffic?
- **502 source**: Is this definitely your code returning 502, or could it be the load balancer timing out waiting for your service?

---

## Recommended Diagnostic Path

Start **here**, in this order:

### 1. **Confirm the 502 source** (5 min, eliminates 50% of possibilities)
   - Check reverse proxy/load balancer logs. Are *they* returning 502, or is your application?
   - If LB logs show `upstream_response_time` = timeout before 502, you're looking at slow/hanging responses, not crashes.
   - If your app logs show no request at all, the connection is dying before your code sees it.

### 2. **Correlate with resource exhaustion** (10 min, eliminates another 25%)
   - At each 502 timestamp: CPU, memory, goroutines (or thread count), open file descriptors, database connections.
   - Plot these on the same timeline as 502 errors. **Spikes don't have to be huge** — a small sustained creep over an hour can flip into failure suddenly.
   - Check for connection pool saturation specifically (database, Redis, external APIs).

### 3. **Check downstream timeouts** (15 min, often the culprit)
   - Do 502s correlate with slow or failed requests to databases, caches, or external services?
   - Set up a quick metric: `P99 latency to [each dependency]` over time. If any of them spike around 502 times, you've found it.
   - Check for cascading timeouts: service A calls B calls C; C hangs, B times out waiting for C, A times out waiting for B, client gets 502.

### 4. **Look for memory/connection leaks** (20 min, systematic)
   - Memory: Is baseline memory creeping upward across the uptime of the process? Does a restart "fix" it for an hour?
   - Connections: Are idle connections being cleaned up, or accumulating? Check netstat/ss on the box during normal operation.
   - Goroutines: If your app logs goroutine count, does it grow monotonically before each 502?

### 5. **Identify request patterns** (20 min, narrow the scope)
   - Filter logs to only 502 requests. Do they share:
     - An endpoint or path?
     - A header or user cohort?
     - A request size or complexity?
   - If 502s cluster on one endpoint, you've narrowed the blast radius enormously.

---

## The Artifact: A Diagnostic Checklist

Once you've run steps 1–2, you'll know roughly where to look. **Next prompt** should include:
- Whether 502 is from your app or the LB
- Whether resource exhaustion is visible
- Whether downstream latency spikes match 502 times

Then I can give you specific queries/code to investigate the most likely culprit (e.g., "connection pool leaks" vs. "hanging requests to database").

**What would be most useful right now: do you have observability in place already, or do you need help setting up metrics/tracing first?**