**Operating from: Upper-Right (Build + Verify)**

### What I understand you're asking
A `docker-compose.yml` that spins up Postgres 16 and Redis 7 for local development, with standard ports exposed and data persistence for the database.

<assumptions>
  <project>You're starting a new dev environment or don't have strong opinions about compose structure yet</project>
  <task>You want a minimal, working compose file you can commit and share with your team</task>
  <operator>You're comfortable with Docker and docker-compose basics; you own verification (testing the stack locally)</operator>
</assumptions>

### The artifact

```yaml
version: '3.9'

services:
  postgres:
    image: postgres:16-alpine
    container_name: postgres_dev
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres  <!-- assumed: change this in .env or production -->
      POSTGRES_DB: dev_db  <!-- assumed: correct database name for your project -->
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
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
  redis_data:
```

### What I'm confident about
- Postgres 16 and Redis 7 images exist and are stable (using `-alpine` for smaller footprint)
- Standard ports (5432 for Postgres, 6379 for Redis) are correct
- Volume mounts will persist data across container restarts
- Healthchecks will help you catch startup issues in scripts

### What I'd double-check
- **Postgres credentials**: The hardcoded `postgres:postgres` is fine for dev, but consider moving to a `.env` file if you're sharing this with a team. Environment variable substitution:
  ```yaml
  environment:
    POSTGRES_USER: ${POSTGRES_USER:-postgres}
    POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-postgres}
  ```
- **Database name**: I assumed `dev_db` — change `POSTGRES_DB` to match what your app expects
- **Redis persistence**: `--appendonly yes` enables AOF (append-only file). If you don't need persistence for dev, remove it and the `command` line entirely
- **Alpine vs. standard**: I used `-alpine` images (smaller, faster to pull). If you need specific extensions or libraries, switch to `postgres:16` or `redis:7` (standard)