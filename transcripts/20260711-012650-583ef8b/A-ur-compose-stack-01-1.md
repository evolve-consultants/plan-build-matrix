# Docker Compose Dev Stack: Postgres 16 + Redis 7

```yaml
version: '3.9'

services:
  postgres:
    image: postgres:16-alpine
    container_name: dev_postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres  # ⚠️  ASSUMED: Using default creds for dev only
      POSTGRES_DB: dev_db          # ⚠️  ASSUMED: Initial database name
      POSTGRES_INITDB_ARGS: "--encoding=UTF8"
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - dev_network

  redis:
    image: redis:7-alpine
    container_name: dev_redis
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes  # ⚠️  ASSUMED: Persistence enabled
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - dev_network

volumes:
  postgres_data:
  redis_data:

networks:
  dev_network:
    driver: bridge
```

## Assumptions & Notes

| Item | Assumption | Rationale |
|------|-----------|-----------|
| **Postgres user/pass** | `postgres:postgres` | Standard dev defaults; change for production |
| **Initial DB name** | `dev_db` | Adjust to your app's needs |
| **Redis persistence** | Enabled (`--appendonly yes`) | Data survives container restarts |
| **Alpine images** | Used for both | Smaller footprint for dev; remove if you need full libc |
| **Health checks** | Included | Services wait for readiness before dependent services start |
| **Shared network** | `dev_network` | Allows container-to-container DNS (e.g., `postgres:5432`) |

## Quick Start

```bash
docker-compose up -d
docker-compose ps
docker-compose logs -f
docker-compose down -v  # Remove volumes too
```

## Connection Strings

- **Postgres**: `postgresql://postgres:postgres@localhost:5432/dev_db`
- **Redis**: `redis://localhost:6379`

(Use `postgres:5432` and `redis:6379` from within containers)