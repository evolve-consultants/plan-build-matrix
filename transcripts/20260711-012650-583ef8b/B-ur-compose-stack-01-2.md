**Operating from: Upper-Right (Build + Verify)**

### What I understand you're asking
A docker-compose file that spins up Postgres 16 and Redis 7 for local development, with standard ports exposed and Postgres data persisted across container restarts.

<assumptions>
  <project>Standard Docker setup; no custom networking or image requirements; assumes you have Docker and docker-compose installed</project>
  <task>You need a minimal, working dev environment you can `docker-compose up` and start using immediately</task>
  <operator>You're comfortable with docker-compose syntax and can modify this if needed; you own data safety (this is dev, not production)</operator>
</assumptions>

### The artifact

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16
    container_name: dev_postgres
    environment:
      POSTGRES_USER: postgres          <!-- assumed: change if you need a different user -->
      POSTGRES_PASSWORD: postgres      <!-- assumed: change for any real use -->
      POSTGRES_DB: dev_db              <!-- assumed: change if you need a different default DB -->
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
    image: redis:7
    container_name: dev_redis
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
- Standard ports (5432 for Postgres, 6379 for Redis) are exposed and accessible from your host
- Postgres data persists in the `postgres_data` volume; stopping/starting containers won't lose it
- Healthchecks allow you to wait for services to be ready before running your app
- Both services use official, minimal images

### What I'd double-check
- **Postgres credentials**: The username, password, and initial DB name are hardcoded. For dev this is fine, but don't commit real passwords. Consider a `.env` file if multiple people use this.
- **Volume driver**: The `postgres_data` volume uses Docker's default driver (usually `local`). On some setups (Windows/Mac with Docker Desktop) this may have performance implications. If you notice slow queries, try a bind mount instead: `- ./postgres_data:/var/lib/postgresql/data`
- **Redis persistence**: Redis is in-memory only here. If you need data to survive container restarts, add `- redis.conf:/usr/local/etc/redis/redis.conf` and create a config file with `appendonly yes`.