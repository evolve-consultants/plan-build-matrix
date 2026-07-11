# docker-compose.yml

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: dev_postgres
    environment:
      POSTGRES_USER: devuser
      POSTGRES_PASSWORD: devpassword  # ⚠️ ASSUMPTION: Using weak password for local dev
      POSTGRES_DB: devdb
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U devuser"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: dev_redis
    ports:
      - "6379:6379"
    # ⚠️ ASSUMPTION: No persistence configured for Redis (data lost on restart)
    # Uncomment below for persistence:
    # volumes:
    #   - redis_data:/data
    # command: redis-server --appendonly yes
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
  # redis_data:  # ⚠️ ASSUMPTION: Commented out; uncomment if you want Redis persistence

networks:
  default:
    name: dev_network
```

## Assumptions Flagged:

1. **Postgres credentials** — Using `devuser`/`devpassword`. Replace with secure values for production or shared environments.
2. **Postgres DB name** — Assumes you want a default `devdb`. Change if needed.
3. **Alpine images** — Using lightweight alpine variants. Switch to full images if you need specific tools.
4. **Redis persistence** — Disabled by default (commented out). Data is lost on container restart. Uncomment if you want persistent storage.
5. **No password on Redis** — Redis has no authentication. Safe for local dev, dangerous otherwise.
6. **Network** — Created automatically. Services can reach each other via `postgres:5432` and `redis:6379`.
7. **Health checks** — Included but not blocking startup. Remove if you don't need them.

## Quick start:
```bash
docker-compose up -d
docker-compose down -v  # Removes volumes on cleanup
```