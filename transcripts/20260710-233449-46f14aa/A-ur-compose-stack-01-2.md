```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: dev-postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres  # ⚠️ ASSUMPTION: Using default password for local dev
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
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - dev-network
    # ⚠️ ASSUMPTION: No persistence for Redis (in-memory only)
    # Uncomment below for RDB snapshots:
    # command: redis-server --appendonly yes
    # volumes:
    #   - redis_data:/data

volumes:
  postgres_data:
  # redis_data:  # Uncomment if enabling Redis persistence

networks:
  dev-network:
    driver: bridge
```

## Assumptions Flagged:

| Assumption | Risk | How to Override |
|-----------|------|-----------------|
| Postgres password `postgres` | **High** - insecure for any shared env | Set `POSTGRES_PASSWORD` env var or use `.env` file |
| Database name `dev_db` | Low | Change `POSTGRES_DB` value |
| No Redis persistence | Medium - data lost on restart | Uncomment `command` and `redis_data` volume |
| Alpine images | Low - smaller but fewer tools | Use `postgres:16` or `redis:7` for full variants |
| Services on same network | Low - assumes containerized clients | Remove `networks` if connecting from host machine |

## Usage:

```bash
docker-compose up -d
docker-compose down
docker-compose logs -f postgres
```

For production-like security, use a `.env` file:
```bash
POSTGRES_PASSWORD=your_secure_password
```