```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16
    container_name: dev_postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres  # ⚠️ ASSUMPTION: Using default password for dev only
      POSTGRES_DB: dev_db           # ⚠️ ASSUMPTION: Default database name
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
    # ⚠️ ASSUMPTION: Redis runs in-memory only (no persistence)
    # Add volumes if you want RDB/AOF persistence
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
    driver: local
```

## Key Assumptions Flagged:

| Item | Assumption | Notes |
|------|-----------|-------|
| **Postgres credentials** | `postgres/postgres` | Change for any shared/production use |
| **Postgres DB name** | `dev_db` | Adjust to your project needs |
| **Redis persistence** | Disabled (in-memory only) | Add `command: redis-server --appendonly yes` + volumes if you need data survival across restarts |
| **Network** | Default bridge | Services auto-discover via container names |
| **Container names** | `dev_postgres`, `dev_redis` | Adjust if running multiple stacks |

## Quick start:
```bash
docker-compose up -d
docker-compose logs -f
docker-compose down  # stops and removes containers, keeps volumes
docker-compose down -v  # also removes volumes
```

Want me to add Redis persistence, environment file support, or anything else?