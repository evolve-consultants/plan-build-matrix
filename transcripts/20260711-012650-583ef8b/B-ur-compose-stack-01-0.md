**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
A `docker-compose.yml` that spins up Postgres 16 and Redis 7 for local development, with data persistence for Postgres and default ports exposed.

<assumptions>
  <project>You don't have a dev stack running yet; this is a fresh setup or migration</project>
  <task>You want a minimal, fast dev environment that survives container restarts</task>
  <operator>You're comfortable with docker-compose basics and can run `docker-compose up`</operator>
</assumptions>

### What I'm unsure of
- **Volume location**: Should the Postgres data live in a named volume (cleaner, portable) or a bind mount to a local directory (easier to inspect/backup)?
- **Authentication**: Do you need a specific Postgres username/password, or is `postgres`/`postgres` fine for dev?
- **Networking**: Should these be accessible only to other containers in the compose stack, or exposed to your host machine (already assumed — ports 5432 and 6379)?
- **Resource limits**: Any memory/CPU constraints, or unlimited?
- **Init data**: Do you need either service to load seed data on startup, or just empty?

### Here's a rough draft (Option A: named volumes, minimal config)

```yaml
version: '3.9'

services:
  postgres:
    image: postgres:16-alpine
    container_name: dev_postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: dev_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: dev_redis
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

**Why this approach:**
- Named volume survives `docker-compose down` but is hidden from the filesystem (clean)
- Alpine images are small (faster pulls)
- Healthchecks let you wait for services to be ready
- No auth required for Redis (standard for dev)
- Minimal, readable config

### Alternative (Option B: bind mount instead)

```yaml
volumes:
  postgres:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: ./data/postgres
```

Use this if you want to inspect/backup the data folder directly or commit it to version control.

### Alternative (Option C: custom Postgres config)

If you need to override Postgres settings (shared buffers, max connections, etc.), add:

```yaml
postgres:
  ...
  volumes:
    - postgres_data:/var/lib/postgresql/data
    - ./postgres.conf:/etc/postgresql/postgresql.conf  # bind mount your config
  command: postgres -c config_file=/etc/postgresql/postgresql.conf
```

### Next prompt should include
- Which volume approach (named or bind mount)?
- Do the default Postgres credentials work, or do you need specific ones?
- Should I add anything else (pgAdmin UI, environment file for credentials, resource limits)?
- Any seed data or initialization scripts?