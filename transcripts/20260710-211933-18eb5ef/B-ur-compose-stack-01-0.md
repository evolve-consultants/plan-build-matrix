**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
A `docker-compose.yml` that spins up Postgres 16 and Redis 7 for local development, with Postgres data persisted across container restarts, both on standard ports.

<assumptions>
  <project>You're starting a new project or setting up a fresh dev environment; no existing compose file or infrastructure constraints</project>
  <task>You want a minimal, working dev stack ready to use immediately with sensible defaults</task>
  <operator>You're comfortable with Docker Compose basics but want to move fast without customizing; you own deciding whether to add things like health checks, resource limits, or networking tweaks</operator>
</assumptions>

### What I'm unsure of
- **Volume location**: Should Postgres data live in a named volume (cleaner, portable) or bind to a local directory (easier to inspect)? Named volumes are standard for dev but some teams prefer bind mounts.
- **Environment setup**: Do you need environment variables in the compose file itself, or are you passing them in at runtime / via `.env`?
- **Postgres initialization**: Do you need any custom init scripts (schema, seed data), or is a blank database fine?
- **Redis persistence**: Do you want Redis data persisted too (RDB or AOF), or is in-memory-only acceptable for dev?

### Here's a working draft (Option A: Named volumes, minimal config)

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

### Alternatives I considered

**B: Bind mount + explicit init directory**  
If you want to inspect Postgres files directly or version-control init SQL:
```yaml
volumes:
  - ./postgres_data:/var/lib/postgresql/data
  - ./init.sql:/docker-entrypoint-initdb.d/init.sql
```
Best when: you're committing seed data or need to inspect the raw PG files.

**C: Redis with persistence enabled**  
If you want Redis data to survive restarts:
```yaml
redis:
  command: redis-server --appendonly yes
  volumes:
    - redis_data:/data
```
Best when: you're testing Redis functionality that depends on historical data.

### Recommendation
**Option A** — it's the dev standard. Named volumes are portable, don't clutter your repo, and Postgres restarts cleanly. Redis in-memory is fine for dev unless you're explicitly testing persistence.

### Next prompt should include
- Whether you want Redis persistence (if yes, switch to Option C)
- Whether you're using init scripts or seed data (if yes, add the init volume)
- Preference between named and bind mount for Postgres (if bind mount, I'll add the path)
- Whether you want me to flesh out a `.env` file template for credentials