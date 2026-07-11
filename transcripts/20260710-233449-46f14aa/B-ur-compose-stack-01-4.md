**Operating from: Upper-Right (Build + Verify)**

### What I understand you're asking
A working docker-compose.yml that spins up Postgres 16 and Redis 7 for local development, with data persistence for the database and standard ports exposed.

<assumptions>
  <project>You're starting fresh or don't have existing compose infrastructure I need to integrate with</project>
  <task>You want a minimal, correct dev stack ready to use immediately</task>
  <operator>You can verify the compose file works by running `docker-compose up` and connecting clients to localhost</operator>
</assumptions>

### The artifact

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16
    container_name: dev_postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres  <!-- assumed: acceptable for local dev; rotate if exposed -->
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
    image: redis:7
    container_name: dev_redis
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes  <!-- assumed: you want persistence; remove if not needed -->

volumes:
  postgres_data:
    driver: local
```

### What I'm confident about
- Ports (5432, 6379) are standard and correct
- Postgres volume persists data across container restarts
- Healthcheck ensures Postgres is ready before dependents start
- Both images are official and stable

### What I'd double-check
- **Default Postgres credentials** (`postgres`/`postgres`): fine for local dev, but if this ever gets shared or pushed, rotate them. Consider using a `.env` file instead of hardcoding.
- **Redis persistence mode** (`appendonly yes`): I included it to match typical dev expectations, but if you don't need durability or want faster iteration, you can remove the `command` line entirely.
- **Container names**: `dev_postgres` and `dev_redis` are arbitrary. Change if you have naming conventions.

### To use this
```bash
docker-compose up -d
# Verify
docker-compose logs postgres  # check healthcheck
docker exec dev_redis redis-cli ping  # should return PONG
psql -h localhost -U postgres -d dev_db  # should connect
```