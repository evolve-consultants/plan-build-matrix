**Operating from: Bottom-Right (Build + Quality)**

### Confirming before I proceed
These are the key assumptions I'm acting on. If any are wrong, say so:
- Postgres credentials: user `postgres`, password `postgres`, db `app` — dev-only, not meant for anything security-sensitive
- Redis has **no** persistent volume (you only asked for Postgres) and no password/auth
- Standard ports means `5432:5432` and `6379:6379`, exposed to host
- No app/service container included — this is just the two data stores
- `restart: unless-stopped` is acceptable for a dev stack (so they survive daemon restarts but you can still stop them manually)
- Docker Compose v2 syntax (no `version:` key needed)

<assumptions>
  <project>No existing docker-compose.yml or project context provided — this is a standalone file.</project>
  <task>You want a minimal, working local dev environment for Postgres + Redis, not a production configuration.</task>
  <operator>Comfortable editing env vars/credentials directly in the file for local use.</operator>
</assumptions>

### The artifact

```yaml
services:
  postgres:
    image: postgres:16
    container_name: postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: app
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    container_name: redis
    restart: unless-stopped
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```