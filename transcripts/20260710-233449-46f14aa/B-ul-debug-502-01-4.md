**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You have a production API that's returning 502 Bad Gateway responses roughly every hour with no visible pattern, and you need a framework for debugging it. You're asking for the initial investigation strategy, not a fix yet.

<assumptions>
  <project>You have observability in place (logs, metrics, traces) but haven't found the root cause yet. The service is deployed to a cloud platform or on-prem infrastructure with multiple instances. You have access to application code and server infrastructure.</project>
  <task>You need to narrow down whether this is an application issue, infrastructure issue, external dependency issue, or load-triggered issue before diving deep.</task>
  <operator>You're looking for a systematic approach that doesn't require redeploying or making changes yet — you want to know what to look at first.</operator>
</assumptions>

### What I'm unsure of
- **Observability**: Do you have distributed tracing (Datadog, Jaeger, etc.), or just logs and basic metrics? This changes what questions we can answer.
- **Scale**: How many instances/processes are running? Does the 502 always come from the same one, or different ones?
- **External dependencies**: Does your API call databases, message queues, or external services? Or is it mostly self-contained?
- **Deployment cadence**: Has anything changed in the last week (code, config, traffic pattern, dependency versions)?

### Options

| | Upside | Downside | Best when |
|---|---|---|---|
| **A: Start with application logs** | Fast, requires no new tools, catches app crashes/panics/timeouts immediately | May miss infrastructure issues, noisy if you don't filter right | You have good structured logging and the 502 is happening *during* the request |
| **B: Start with infrastructure metrics** | Reveals resource exhaustion (CPU, memory, file descriptors, disk), network issues | Slower to correlate with 502s, can be a rabbit hole | You suspect load, memory leaks, or resource limits |
| **C: Start with upstream/downstream dependencies** | Catches cascading failures, database overload, external API timeouts | Time-consuming if you have many dependencies, may not be the cause | You've ruled out the app itself or seen timeout patterns |
| **D: Start with request tracing (if available)** | Shows you exactly where in the call stack the 502 originates, reveals cascade failures | Requires existing tracing infrastructure, adds latency to queries | You have Datadog/Jaeger/similar already running |

### Recommendation

**Start with Option A + the infrastructure metrics that correlate exactly with 502s** (Option B's framing, not its full depth).

Here's why: 502s are typically either application crashes or upstream timeouts. A quick scan of logs at the exact timestamp(s) of 502s will tell you if the app is even still running. If logs are clean, you pivot to "what was the infra state at that moment?" — memory? CPU? Open connections?

This path gets you an answer in 15 minutes instead of hours, and it rules out 70% of possibilities.

### Exact next steps to take right now

1. **Get the 502 timestamps**: Check your load balancer or reverse proxy logs for when 502s occurred. Get 2–3 examples with exact timestamps.

2. **Check application logs at those timestamps**:
   ```
   # If JSON logs:
   grep -A5 -B5 "TIMESTAMP" app.log | grep -E "panic|fatal|error|timeout"
   
   # Or query your log aggregator with:
   timestamp >= EXACT_502_TIME AND timestamp <= EXACT_502_TIME + 5s
   ```

3. **Check if the app was even running**:
   - Did the process crash and restart?
   - Does the request appear in logs at all, or does it vanish mid-processing?
   - If it appears and completes normally in logs, the 502 is coming from upstream (load balancer, reverse proxy, or a timeout between them).

4. **Grab infrastructure snapshot at that exact time**:
   - CPU % (all processes, not just yours)
   - Memory % (heap for your app, system-wide free)
   - Open file descriptors or connection count
   - Network saturation or errors
   - Disk I/O or space

### Next prompt should include
- Answer to the observability question (what logging/tracing tools do you have?)
- The 502 timestamps (or a pattern if there is one — certain time of day, after a deploy, etc.)
- Whether logs at those timestamps show the request at all, and what the last log line before 502 looks like
- Infrastructure constraints you know about (how many instances, what's the max expected load?)

Once you give me those, we'll either have a smoking gun or I'll have you collect 2–3 more specific signals to narrow it down further.