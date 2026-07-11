**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You want a `docker-compose.yml` that spins up a local dev environment with Postgres 16 and Redis 7 on their standard ports (5432 and 6379), with Postgres data persisting across container restarts.

<assumptions>
  <project>You're starting a new dev stack or standardizing an existing one; no existing compose file to extend</project>
  <task>You want a minimal, working compose file ready to `docker-compose up` immediately</task>
  <operator>You're comfortable with Docker Compose and know how to manage volumes and networking; you own verification of whether this matches your actual needs</operator>
</assumptions>

### What I'm unsure of
- **Postgres initialization**: do you need a specific database created on startup, or is the default `postgres` db enough?
- **Redis persistence**: do you need Redis data to survive restarts (RDB snapshots, AOF), or is it okay if it's ephemeral?
- **Environment variables**: do you want to set Postgres credentials (password, user) explicitly, or use defaults?
- **Network mode**: are other services (app containers) going to live in this compose, or is this stack standalone?

### Here's a minimal draft (Option A: no persistence, defaults)

```yaml
version: '3.9'

services:
  postgres:
    image: postgres:16-alpine
    container_name: dev_postgres
    environment:
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    container_name: dev_redis
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

**Flags in this version:**
- `POSTGRES_PASSWORD: postgres` — you probably want to change this or use a `.env` file
- `POSTGRES_USER` defaults to `postgres`
- Redis has **no persistent volume** — data is lost on container stop
- Both services restart automatically if they crash (`restart: unless-stopped` not set, so they won't auto-restart)

### Option B: Production-adjacent (persistent Redis, env vars, restart policy)

```yaml
version: '3.9'

services:
  postgres:
    image: postgres:16-alpine
    container_name: dev_postgres
    environment:
      POSTGRES_USER: ${DB_USER:-postgres}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-postgres}
      POSTGRES_DB: ${DB_NAME:-dev}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-postgres}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: dev_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped
    command: redis-server --appendonly yes
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
  redis_data:
```

**Flags in this version:**
- Reads DB credentials from env vars (`.env` file or shell exports) with sensible defaults
- Redis runs with AOF persistence (`--appendonly yes`) — slightly slower but safer
- Both have `restart: unless-stopped` and health checks (good for dev, catches hangs)
- `POSTGRES_DB` creates a named database on startup instead of just `postgres`

### Recommendation
**Start with Option A** if you just need it running right now and don't care about Redis data surviving restarts.

**Use Option B** if you want to avoid typing credentials every time, or if you're building toward a pattern you'll use in staging/prod.

Either way, create a `.env` file in the same directory:
```
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_NAME=dev
```

Then `docker-compose up -d` and verify with:
```bash
docker-compose ps
docker exec dev_postgres psql -U postgres -d dev -c "\dt"
docker exec dev_redis redis-cli ping
```

### Next prompt should include
- Whether you need Redis or Postgres data to persist
- Whether you want a specific initial database created (and with what schema/seed data)
- Whether other services (an app container) will live in this same compose file
- Your preference: minimal and fast (Option A) or slightly more robust (Option B)?