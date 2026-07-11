# docker-compose.yml
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: dev-postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres  # ⚠️ ASSUMED: Using default creds for dev
      POSTGRES_DB: dev_db          # ⚠️ ASSUMED: Initial database name
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
    container_name: dev-redis
    ports:
      - "6379:6379"
    # ⚠️ ASSUMED: No persistence; Redis data lost on container restart
    # Uncomment below if you want RDB persistence:
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
  # redis_data:  # ⚠️ UNCOMMENT if enabling Redis persistence

```

## Key Assumptions & Notes:

| Item | Assumption | Why |
|------|-----------|-----|
| **Postgres creds** | `postgres:postgres` | Standard dev default; change for any shared/prod use |
| **Initial DB** | `dev_db` | Remove `POSTGRES_DB` if you prefer manual creation |
| **Redis persistence** | Disabled (commented out) | Typical for dev; avoids stale data surprises |
| **Alpine images** | Used for both | Smaller, faster builds; remove `-alpine` if you need full tooling |
| **Healthchecks** | Included | Useful for scripting; remove if not needed |

## Quick Start:
```bash
docker-compose up -d
docker-compose ps
docker-compose logs -f
docker-compose down
```

## To enable Redis persistence:
Uncomment the `volumes` section and `command` line in the redis service.