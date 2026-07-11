# Assumptions
- **Database name, user, password**: Using `devdb`/`devuser`/`devpass` (⚠️ change these)
- **Postgres volume location**: Named volume `postgres_data` (alternative: bind mount to local directory)
- **Redis persistence**: Not enabled (RDB snapshots disabled; use `appendonly yes` if needed)
- **Network**: Default bridge network is sufficient for service-to-service communication
- **Init scripts**: No Postgres init SQL files (add `./init.sql:/docker-entrypoint-initdb.d/init.sql` if needed)

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: dev_postgres
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: devdb              # ⚠️ Change as needed
      POSTGRES_USER: devuser          # ⚠️ Change as needed
      POSTGRES_PASSWORD: devpass      # ⚠️ Change - use .env file in production
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U devuser"]
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
    command: redis-server --appendonly no  # ⚠️ Add persistence if needed
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - dev_network

volumes:
  postgres_data:

networks:
  dev_network:
    driver: bridge
```

## Quick Start
```bash
docker-compose up -d
docker-compose ps
docker-compose logs -f postgres
```

## To Enable Redis Persistence
Replace Redis command with:
```yaml
command: redis-server --appendonly yes
```
And add a volume:
```yaml
volumes:
  - redis_data:/data
```