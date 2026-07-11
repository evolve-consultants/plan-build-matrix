PostgreSQL's default port is **5432**.

A few relevant details:

- This is set in the `postgresql.conf` configuration file via the `port` parameter, and can be changed if needed.
- If you're running multiple PostgreSQL instances on the same machine, each typically needs a unique port (e.g., 5432, 5433, etc.).
- Common connection string format: `postgresql://username:password@localhost:5432/database_name`
- For command-line tools like `psql`, you can specify the port explicitly with `-p 5432` if it's not the default, though it's often omitted since 5432 is assumed.

If you're troubleshooting a connection issue, it's worth checking whether the port has been changed from default, especially in cloud-hosted or containerized environments (like Docker, where port mapping might differ from the internal container port).