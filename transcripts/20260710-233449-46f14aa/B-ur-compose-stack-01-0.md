**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
A `docker-compose.yml` that spins up Postgres 16 and Redis 7 for local development, with data persistence for Postgres and standard ports exposed.

<assumptions>
  <project>You're starting a new dev environment or standardizing an existing one; no existing compose file I need to preserve or extend.</project>
  <task>You want a minimal, working stack that survives container restarts and is ready to use immediately.</task>
  <operator>You have Docker and Docker Compose installed and are comfortable with basic compose patterns.</operator>
</assumptions>

### What I'm unsure of
- **Postgres user/password**: Should I use default `postgres/postgres`, or do you have naming preferences?
- **Volume location**: Should the Postgres volume live in a named volume (easier to manage) or bind-mounted to a local directory (easier to inspect)?
- **Network isolation**: Do both services need to talk to each other, or only to your app? (This affects whether I create an explicit network.)
- **Health checks**: Do you want readiness probes so your app waits for the databases to be ready?
- **Resource limits**: Any CPU/memory constraints for dev, or unlimited?

### Here's a working baseline (Option A)

```yaml
version: '3.9'

services:
  postgres:
    image: postgres:16
    container_name: dev_postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: dev_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7
    container_name: dev_redis
    ports:
      - "6379:6379"
    restart: unless-stopped

volumes:
  postgres_data:
```

**Flags:**
- `POSTGRES_PASSWORD: postgres` — obvious default; change if you need security even in dev
- Named volume `postgres_data` — survives `docker-compose down` but lives in Docker's managed directory; switch to `./postgres_data:/var/lib/postgresql/data` if you want it locally inspectable
- No health checks — Redis starts instantly, but Postgres may take 2–3 seconds; if your app connects immediately on startup, add `healthcheck` blocks
- No resource limits — fine for dev, but add `deploy.resources.limits` if you're memory-constrained

### Alternatives I considered

**Option B: With health checks + bind mount**
```yaml
postgres:
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U postgres"]
    interval: 5s
    timeout: 5s
    retries: 5
  volumes:
    - ./postgres_data:/var/lib/postgresql/data
```
Best if your app starts before Postgres is ready, or you want to inspect the data directory directly.

**Option C: With explicit network + resource limits**
Adds `networks: [dev]` to both services and a `networks: { dev: {} }` top level. Add `deploy.resources.limits: {cpus: '1', memory: 512M}` to constrain. Best if you're running other containers and want isolation.

### Next prompt should include
- Which of those three flags matters most to you (password, volume style, health checks)
- Whether you want the health checks and/or bind mount from Option B
- Any custom database name or user instead of `postgres`