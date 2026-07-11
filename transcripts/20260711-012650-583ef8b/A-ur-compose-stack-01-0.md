# docker-compose.yml - Dev Stack

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: dev-postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres  # ⚠️ ASSUME: Change for production
      POSTGRES_DB: dev_db          # ⚠️ ASSUME: Default DB name
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
    command: redis-server --appendonly yes  # ⚠️ ASSUME: AOF persistence enabled
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - dev-network

volumes:
  postgres_data:

networks:
  dev-network:
    driver: bridge
```

## Key Assumptions Flagged

| Item | Assumption | Why Flag |
|------|-----------|---------|
| **POSTGRES_PASSWORD** | Hardcoded as `postgres` | Never use in real env; use `.env` file instead |
| **POSTGRES_DB** | Auto-creates `dev_db` | Adjust if different DB name needed |
| **POSTGRES_USER** | Defaults to `postgres` | Non-root user may be preferred for prod |
| **Redis persistence** | AOF enabled (`--appendonly yes`) | Dev convenience; adjust for performance needs |
| **Alpine images** | Using slim `alpine` variants | Trade-off: smaller size vs. fewer tools for debugging |
| **Container names** | Hard-coded names | May conflict if running multiple stacks |
| **Healthchecks** | Included | Useful for dev; remove if overhead matters |

## Usage

```bash
# Start
docker-compose up -d

# Verify
docker-compose ps

# Connect to Postgres
psql -h localhost -U postgres -d dev_db

# Connect to Redis
redis-cli -h localhost

# Logs
docker-compose logs -f postgres
docker-compose logs -f redis

# Stop & clean
docker-compose down
docker-compose down -v  # Also remove volumes
```

## For Production, Also Consider:
- Use `.env` file for secrets
- Non-root users for both services
- Resource limits (`mem_limit`, `cpus`)
- Backup strategy for Postgres volume
- Network isolation (don't expose to 0.0.0.0)