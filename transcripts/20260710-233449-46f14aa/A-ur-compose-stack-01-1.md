```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: dev_postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres  # ⚠️ ASSUMPTION: Using default password for local dev
      POSTGRES_DB: dev_db          # ⚠️ ASSUMPTION: Creating a default dev database
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
    command: redis-server --appendonly yes  # ⚠️ ASSUMPTION: AOF persistence enabled
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

## Key Assumptions:

1. **Postgres credentials** - Using `postgres:postgres` (NOT production-safe)
2. **Default database** - Creating `dev_db` on startup
3. **Redis persistence** - Enabled AOF mode for data durability
4. **Alpine images** - Using lighter variants for dev (assumes you don't need full distro)
5. **Internal networking** - Services communicate via `dev_network`; localhost ports exposed for host access
6. **Volume naming** - Using Docker's default volume driver (local)

## To use:
```bash
docker-compose up -d
docker-compose logs -f
docker-compose down  # keeps volumes
docker-compose down -v  # removes volumes
```