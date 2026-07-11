**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You have a production API returning 502 Bad Gateway errors roughly once per hour with no obvious trigger. You need a systematic approach to diagnose the root cause.

<assumptions>
  <project>Standard web service stack (language, framework, deployment model unknown). Single or multiple instances. Some monitoring in place but apparently not granular enough to pinpoint the issue yet.</project>
  <task>You want to move from "it's broken sometimes" to "here's what's causing it" so you can fix it or roll back the culprit.</task>
  <operator>You have access to logs, metrics, and infrastructure. You can deploy changes or rollbacks. The intermittent nature is frustrating but also suggests the problem is reproducible under specific conditions, not random.</operator>
</assumptions>

### What I'm unsure of
- **Stack**: Language, framework, deployment (containerized, VMs, serverless)?
- **Load**: Is traffic volume consistent? Traffic spikes correlated with 502s?
- **Changes**: Did anything deploy recently (code, dependencies, infra config)?
- **Observability**: What monitoring/logging do you have now? (metrics, structured logs, APM, error tracking?)
- **502 source**: Is it from your service itself, a reverse proxy/load balancer, or downstream?

These matter because the diagnostic path differs significantly depending on the answer.

### Three diagnostic starting points

| | Start with | Why | Best when |
|---|---|---|---|
| **A: Recent changes** | Git log, recent deploys, dependency updates | 502s often appear after code/config changes. Fastest elimination. | You deployed something in the last few hours/days. |
| **B: Observability first** | Logs + metrics around 502 timestamps | You need to see what the service was doing at failure time. Prerequisite for everything else. | You have structured logs and can correlate by timestamp. |
| **C: Infrastructure health** | Resource usage (CPU, memory, connections, disk) at failure time | 502s often mean "upstream can't reach downstream" — resource exhaustion or crashes cause this. | You suspect resource limits, connection pool exhaustion, or process restarts. |

### Recommendation
**Start with B (Observability), then split into A and C in parallel.**

Here's why: You need to see what's happening at the moment of failure before anything else makes sense. Once you have that visibility, A and C branch out in different directions depending on what the logs show.

- If logs show request errors or exceptions → A (recent changes)
- If logs show resource spikes or process restarts → C (infrastructure)
- If logs are silent but metrics show load → upstream/proxy issue (different path)

### Next prompt should include
1. **What observability do you have?** (structured logs? APM? metrics system? what can you query by timestamp?)
2. **Did anything change recently?** (deploy, dependency, infrastructure config)
3. **What's your stack?** (language, framework, deployment model)
4. **What do your 502 error logs show?** (or: can you point me to them, or do you need help querying?)

Once I have those, I can walk you through extracting the signal from the noise.