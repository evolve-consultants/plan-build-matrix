# Debugging Intermittent 502s

Start with **three parallel investigations** since there's no obvious pattern:

## 1. **Isolate the 502 source** (15 min)
- Is it your load balancer, reverse proxy (nginx/HAProxy), or actual app servers returning 502?
- Check logs at each layer—they tell very different stories
- A 502 from nginx means the upstream didn't respond in time or refused the connection
- If it's your app returning 502, that's different (see below)

## 2. **Check resource exhaustion** (immediate)
```bash
# During/after a 502 incident:
- Memory: free, oom-killer logs
- CPU: saturation, context switches
- Connections: netstat -an | grep ESTABLISHED | wc -l
- Disk I/O: iostat, slow queries
- File descriptors: lsof, ulimit
```
502s often spike when something quietly consumes resources. One bad query, memory leak, or connection leak creates a cascading failure.

## 3. **Examine upstream behavior**
- **Timeout settings**: What's your reverse proxy timeout vs. app response time? A slow 10-second request hitting a 5-second timeout = 502
- **Connection pool exhaustion**: Are you running out of connections to upstream servers?
- **Health checks**: Are your backends flapping in/out of rotation?

## 4. **Application-level signals**
Look for patterns *around* 502 timestamps:
- Error spike (exceptions, panics)?
- Slow requests that saturate worker threads?
- Database connection pool exhaustion?
- External API timeouts cascading?

## High-ROI quick wins
1. **Increase timeout slightly** if requests are legitimately slow (and you've ruled out actual hangs)
2. **Add request queuing visibility**—is your load balancer rejecting requests because backends are full?
3. **Enable detailed logging** on the reverse proxy layer with upstream response times
4. **Check for memory leaks** in your app (restart frequency patterns?)

What's your stack (language, proxy, orchestration)? That shapes where the 502 is likely coming from.