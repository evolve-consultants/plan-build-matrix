**Operating from: Upper-Right (Build + Verify)**

### What I understand you're asking
A docker-compose file for local development with Postgres 16 and Redis 7, exposed on standard ports (5432 and 6379), with Postgres data persisted to disk between container restarts.

<assumptions>
  <project>You're starting fresh — no existing compose file, no special networking needs, no multi-host setup</project>
  <task>You want a minimal, working dev stack that mirrors production port expectations</task>
  <operator>You can run Docker locally and are comfortable with basic compose syntax; you'll handle .env secrets yourself or use defaults for dev</operator>
</assumptions>

### The artifact

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: postgres_dev
    environment:
      POSTGRES_USER: postgres                    <!-- assumed: dev default user -->
      POSTGRES_PASSWORD: postgres                <!-- assumed: dev default password -->
      POSTGRES_DB: dev_db                        <!-- assumed: default DB name; change as needed -->
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
    container_name: redis_dev
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

### What I'm confident about
- Port mappings match standard Postgres (5432) and Redis (6379)
- `postgres_data` volume persists Postgres state across `docker-compose down`
- Alpine images keep footprint small for dev
- Healthchecks let you wait for services to be ready before running migrations or tests

### What I'd double-check
- **POSTGRES_PASSWORD**: This is hardcoded to `postgres`. For any shared dev environment, use a `.env` file instead:
  ```yaml
  environment:
    POSTGRES_USER: ${POSTGRES_USER:-postgres}
    POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-postgres}
    POSTGRES_DB: ${POSTGRES_DB:-dev_db}
  ```
  Then create `.env` with real values and add it to `.gitignore`.
- **Database name**: I assumed `dev_db`. Change `POSTGRES_DB` if you want a different default.
- **Persistence location**: On Docker Desktop (Mac/Windows), volumes live in the Docker VM. On Linux, they're local. If you need the actual filesystem path, ask and I'll clarify.