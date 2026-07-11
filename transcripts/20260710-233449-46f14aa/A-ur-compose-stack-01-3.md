# docker-compose.yml

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: dev-postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres  # ⚠️ ASSUMPTION: Default dev password
      POSTGRES_DB: dev_db          # ⚠️ ASSUMPTION: Default database name
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
      - dev-network

  redis:
    image: redis:7-alpine
    container_name: dev-redis
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes  # ⚠️ ASSUMPTION: AOF persistence enabled
    volumes:
      - redis_data:/data                     # ⚠️ ASSUMPTION: Redis persistence desired
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - dev-network

volumes:
  postgres_data:
  redis_data:

networks:
  dev-network:
    driver: bridge
```

## Assumptions Flagged:

| Assumption | Alternative |
|-----------|-------------|
| **Postgres password: `postgres`** | Use `.env` file or secrets for security |
| **Database name: `dev_db`** | Change to match your actual dev database name |
| **Redis AOF persistence** | Remove `--appendonly yes` if you don't need persistence |
| **Redis data volume** | Remove `redis_data` volume if ephemeral is preferred |
| **Alpine images** | Use `postgres:16` or `redis:7` (full) if you need specific tools |
| **Shared network** | Services communicate via `postgres:5432` and `redis:6379` internally |

## Quick start:
```bash
docker-compose up -d
docker-compose down -v  # Remove everything including volumes
```