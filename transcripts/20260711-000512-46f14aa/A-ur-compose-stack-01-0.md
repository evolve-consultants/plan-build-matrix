# docker-compose.yml

```yaml
version: "3.9"

services:
  postgres:
    image: postgres:16
    container_name: dev_postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: devuser
      POSTGRES_PASSWORD: devpassword
      POSTGRES_DB: devdb
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U devuser -d devdb"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7
    container_name: dev_redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  pgdata:
    driver: local
```

## Assumptions flagged

1. **Credentials**: Used placeholder `devuser` / `devpassword` / `devdb`. Hardcoding creds in compose is fine for local dev but should never be used as-is in shared/prod environments. Consider moving to a `.env` file if you want to avoid committing secrets even for dev.

2. **Ports**: Assumed "standard ports" means default, unmapped host ports:
   - Postgres → `5432:5432`
   - Redis → `6379:6379`
   
   If you already run Postgres/Redis locally, these will conflict — let me know if you want alternate host ports (e.g., `55432:5432`).

3. **No Redis persistence**: Redis is running in default (ephemeral) mode — no AOF/RDB volume, since you only asked for a persistent volume on Postgres. Data will be lost on container removal. Say the word if you want Redis persistence too.

4. **No password on Redis**: Redis has no `requirepass` set — open access within the Docker network. Fine for local dev, not for anything exposed.

5. **Networking**: No custom network defined; both services will share Compose's default bridge network and can reach each other by service name (`postgres`, `redis`). Didn't add an explicit `networks:` block since it's not required for two services.

6. **No pgAdmin/Redis Commander/etc.**: Kept it minimal — just the two requested services. Say if you want a DB admin UI added.

7. **Image tags**: Used `postgres:16` and `redis:7` (latest minor/patch within those majors). Pin to a specific patch version (e.g., `postgres:16.4`) if you need reproducibility across machines/time.

8. **Restart policy**: Set to `unless-stopped` for dev convenience (auto-restart on crash/reboot but not if you manually stop it). Change to `no` if you'd rather containers stay down after a stop.