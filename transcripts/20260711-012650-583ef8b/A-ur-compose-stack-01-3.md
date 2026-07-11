```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: dev_postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres  # ⚠️ ASSUMPTION: Basic dev password
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
      - dev_network

  redis:
    image: redis:7-alpine
    container_name: dev_redis
    ports:
      - "6379:6379"
    # ⚠️ ASSUMPTION: No persistence configured for Redis
    # Add below if you want RDB snapshots:
    # command: redis-server --appendonly yes
    # volumes:
    #   - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - dev_network

volumes:
  postgres_data:
  # redis_data:  # ⚠️ UNCOMMENT if enabling Redis persistence

networks:
  dev_network:
    driver: bridge
```

## Assumptions Flagged:

| Flag | Detail |
|------|--------|
| **Postgres User/Pass** | Using `postgres/postgres` — change for any sensitive work |
| **Database Name** | Creates `dev_db` — adjust to your project needs |
| **Redis Persistence** | Currently disabled (ephemeral). Uncomment volumes if you need data to survive restarts |
| **Alpine Images** | Using `-alpine` variants for smaller footprint — use standard `postgres:16` if you need specific extensions |
| **Healthchecks** | Included but not blocking — services start immediately |
| **Network Isolation** | Uses custom bridge network — both services can reference each other by name |

## Quick Start:
```bash
docker-compose up -d
```

Connect to Postgres: `psql -h localhost -U postgres -d dev_db`  
Connect to Redis: `redis-cli -h localhost`