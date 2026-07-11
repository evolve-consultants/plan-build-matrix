**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
Your production API is intermittently throwing 502s roughly hourly with no visible pattern, and you want a starting point for diagnosis rather than a specific fix.

<assumptions>
  <project>You have some kind of reverse proxy or load balancer (nginx, ALB, Cloudflare, etc.) sitting in front of an application server, and you have access to logs/metrics at both layers, though I don't know the stack.</project>
  <task>You want a systematic diagnostic approach, not just a guess — and this is likely causing real (if intermittent) user impact given you're asking now.</task>
  <operator>You have infra/ops access (can pull LB logs, app logs, deploy history, resource metrics) but haven't yet correlated the 502s against any of those signals.</operator>
</assumptions>

### What I'm unsure of
- What's actually serving the app (nginx, ALB/ELB, Cloudflare, Envoy, etc.) and what's behind it (containers, VMs, serverless)
- Whether you have access to logs/metrics on both the proxy and app side, or only one
- Whether autoscaling, rolling deploys, or scheduled jobs run on a cadence that could line up with "once an hour"
- Whether the 502s correlate with traffic spikes or are steady regardless of load

### Options — where to start looking

| | Upside | Downside | Best when |
|---|---|---|---|
| **A. Correlate timestamps across layers** — pull exact timestamps of 502s and cross-reference against LB logs, app logs, deploy history, and autoscaling events | Cheap, fast, often finds the cause in minutes if it's a restart/deploy/scaling event | Won't help if the cause is subtle (e.g., a slow leak) rather than an event | You suspect something periodic (cron, scaling, health check) |
| **B. Check upstream resource limits** — look for OOM kills, CPU throttling, or process restarts around the 502 timestamps | Directly explains "upstream closed connection" style 502s | Requires access to container/host-level metrics, not just app logs | Your app runs in containers with defined memory/CPU limits |
| **C. Audit timeout/keepalive config mismatches** — compare LB timeout, keepalive, and idle-connection settings against the app server's equivalents | Finds a whole class of 502s caused by the proxy and app disagreeing on how long a connection should live | Doesn't explain crash-based 502s; is a config review, not a live investigation | You haven't touched LB/app timeout settings recently or inherited this setup |
| **D. Add/verify structured logging on 502-adjacent signals** — if logs aren't detailed enough to do A-C, first improve logging (upstream response time, connection reuse, worker PID) before diagnosing further | Sets you up to actually answer the question instead of guessing | Slower — you're instrumenting before you're investigating | Current logs don't have enough detail to correlate anything |

### Recommendation
Start with **Option A**. It's the fastest, requires no new instrumentation, and will either hand you the answer directly (e.g., "every 502 lines up with a deploy") or rule out several causes at once, narrowing where to look next (B or C).

### Next prompt should include
- What's actually in front of your app (nginx/ALB/Cloudflare/etc.) and what runs behind it
- Whether you can pull exact timestamps of the 502s and cross-reference them against deploy/scaling/cron logs
- What you find when you do that correlation — even "nothing lines up" is useful signal and will point us toward B or C