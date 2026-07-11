# Debugging Intermittent 502s

Start with the basics, because intermittent + no pattern usually points to resource exhaustion or cascading failures rather than code bugs.

## Immediate triage (next 30 minutes)

**Check infrastructure metrics during incidents:**
- CPU, memory, disk on your servers/containers
- Network saturation, packet loss
- Database connection pool exhaustion
- Message queue depth (if applicable)
- Load balancer health check failures

**The key:** correlate 502s with *any* metric spike, not just obvious ones. Sometimes it's disk I/O, not CPU.

**Check logs for the actual failure:**
```
502 Bad Gateway typically means:
- Your app server crashed/restarted
- Upstream service (DB, cache, external API) timed out
- Load balancer couldn't reach a healthy backend
```
Look at app logs around the 502 timestamps, not just access logs.

## Second wave (if basics are clean)

**Memory leaks/slow growth:**
- Plot memory usage over hours before incident
- Check for unbounded caches, connection leaks, goroutine leaks

**Dependency timeouts:**
- Are you timing out on DB queries? External APIs? Cache?
- Increase timeouts to see if they're too aggressive, then investigate why queries are slow
- One slow dependency can cascade

**Uneven load distribution:**
- One backend instance consistently slower than others?
- Check logs for long-running requests on specific servers

## The most common culprits

1. **Database connection pool exhausted** — slow queries hold connections
2. **Memory leak** — restarts once/hour might look "random"
3. **Upstream timeout** — you call an API that's flaky
4. **GC pauses** — full GC on a bloated heap can trigger timeouts
5. **Thundering herd** — retry storms or scheduled jobs piling up

## What to instrument NOW

```
- Track: request latency (p50/p95/p99)
- Track: active database connections
- Track: error rate by upstream service
- Track: garbage collection time (if applicable)
- Correlate: 502 rate with any of the above
```

**What do your 502 logs actually show?** That's your next move. "Upstream server not responding" vs "connection refused" vs "timeout" point in very different directions.