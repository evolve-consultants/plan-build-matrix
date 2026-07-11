**Operating from: Bottom-Right (Build + Quality)**

### Confirming before I proceed

These are the key assumptions I'm acting on. If any are wrong, now is the time to say so:

- You want both services to start together and be accessible to a host application or other containers on the same network
- "Standard ports" means Postgres on 5432 and Redis on 6379, exposed to localhost
- Persistent volume means Postgres data survives container restarts; Redis can be ephemeral (common for dev)
- You're running this on a local dev machine (not production, not a remote server)
- No authentication requirements (dev convenience over security)
- You want a single compose file, ready to `docker-compose up`

---

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: dev_postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: dev_db
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

### What's in there

- **Alpine images**: smaller, faster to pull
- **Healthchecks**: let you wait for services to be ready before running app code
- **`postgres_data` volume**: named volume persists across restarts; stored in Docker's managed location
- **Default postgres creds**: `postgres/postgres` on `dev_db` — change these if you're sharing the file
- **No Redis persistence**: Redis runs in-memory (standard for dev caching); add `--appendonly yes` to `redis` command if you want durability

### Next steps

1. Save as `docker-compose.yml` in your project root
2. Run: `docker-compose up -d`
3. Verify: `docker-compose ps` (both should show healthy)
4. Connect locally: `psql -h localhost -U postgres -d dev_db` (or your app's connection string)
5. To stop: `docker-compose down` (data persists)
6. To nuke everything: `docker-compose down -v` (deletes the volume)