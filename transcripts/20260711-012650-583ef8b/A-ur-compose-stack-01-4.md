# docker-compose.yml for Dev Stack

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: dev-postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres  # ⚠️ ASSUMPTION: Using default creds for dev
      POSTGRES_DB: dev_db           # ⚠️ ASSUMPTION: Default DB name
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
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
    driver: local
```

## Assumptions & Notes

| Item | Assumption | Consider |
|------|-----------|----------|
| **Postgres credentials** | User: `postgres`, Password: `postgres` | Use `.env` file for sensitive values in real dev |
| **Postgres DB** | Creates `dev_db` on startup | Modify `POSTGRES_DB` as needed |
| **Alpine images** | Using lightweight Alpine variants | Use full images if you need specific tools |
| **Healthchecks** | Included for both services | Helps orchestration and dependency ordering |
| **Networking** | Using default bridge network | Services auto-discoverable by container name |
| **Volumes** | Only Postgres persisted | Redis is ephemeral (typical for dev) |

## Usage

```bash
docker-compose up -d
docker-compose logs -f
docker-compose down
```

## Better for Production

```yaml
# Add to postgres service:
environment:
  POSTGRES_PASSWORD_FILE: /run/secrets/db_password
secrets:
  db_password:
    file: ./secrets/db_password.txt
```