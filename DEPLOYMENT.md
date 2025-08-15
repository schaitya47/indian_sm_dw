Deployment steps for indian_sm_dw (Mage-AI)

**RECOMMENDED**: Use the Docker Compose approach (see "On‑Prem Deployment Checklist" section) for simpler deployment. The manual Docker commands below are provided for reference but are more complex.

Overview
- Postgres runs as a Docker container with host-mounted data for persistence.
- Mage runs as a Docker container, connected to the same Docker network and using Postgres for metadata via environment variables.
- Secrets (passwords) must be provided at runtime; do NOT bake them into images or commit to git.

Prerequisites (on on-prem host)
- Docker installed and running
- Ports available: 6789 (Mage UI) and a host port for Postgres (default 5432)
- Paths to persist data: /srv/mage_project (project code), /srv/mage_pg (Postgres data)

Step-by-step
1) Create directories and set permissions
   sudo mkdir -p /srv/mage_pg /srv/mage_project
   sudo chmod 700 /srv/mage_pg
   sudo chown "$USER":"$USER" /srv/mage_project

2) Copy project into /srv/mage_project or bind-mount your repo there

3) Start Postgres container (example)
   sudo docker run -d --name mage-postgres \
     -e POSTGRES_USER=postgres \
     -e POSTGRES_PASSWORD=<YOUR_PASSWORD> \
     -e POSTGRES_DB=indian_sm_dw \
     -v /srv/mage_pg:/var/lib/postgresql/data \
     -p 127.0.0.1:5432:5432 \
     --restart unless-stopped \
     postgres:14

4) (Optional) Create a user network so containers can communicate by name
   sudo docker network create mage-net
   sudo docker network connect mage-net mage-postgres

5) Build Mage image from your project root (ensure Dockerfile present)
   cd /srv/mage_project
   sudo docker build -t mymageimage .

6) Run Mage container pointing to Postgres via env var. Provide POSTGRES_PASSWORD at runtime.
   sudo docker run -d --name mage-app --network mage-net \
     -v /srv/mage_project:/app \
     -e MAGE_DATABASE_URL="postgresql://postgres:<YOUR_PASSWORD>@mage-postgres:5432/indian_sm_dw" \
     -p 6789:6789 \
     --restart unless-stopped \
     mymageimage

7) Verify Mage UI accessible at http://<HOST_IP>:6789 and that pipelines/metadata persist after restarts.

Notes and security
- Do not commit passwords; use a .env file or a secrets manager in production.
- Set safe permissions on .env after creating it: chmod 600 /srv/mage_project/.env
- Consider binding Postgres to localhost (127.0.0.1:5432) to avoid exposing it externally.
- Back up Postgres data regularly using pg_dump and archive /srv/mage_project/backups.

Troubleshooting
- If port 5432 is in use, either stop the conflicting service or run Postgres on a different host port (e.g., -p 5433:5432) and update MAGE_DATABASE_URL.
- If image build fails, inspect the last ~30 lines of the build output and adjust requirements or Dockerfile.

Contact
- Keep this document with your repo and update with real passwords or instructions for a secrets manager.

On‑Prem Deployment Checklist (concise)

Follow these steps on the target on‑prem host to deploy the project reliably.

Prerequisites
- Linux server (Ubuntu 22.04 recommended), sudo access.
- Docker and Docker Compose installed. (Install: curl -fsSL https://get.docker.com | sh; sudo apt-get install -y docker-compose-plugin)
- Open ports: 6789 (Mage UI) and optionally 5432 (Postgres) — prefer binding Postgres to localhost for security.

Prepare project on host
1) Clone the repo to the deployment path (example):
   sudo mkdir -p /srv/mage_project && sudo chown $USER:$USER /srv/mage_project
   git clone <your-repo-url> /srv/mage_project
   cd /srv/mage_project

2) Create and edit .env from the example, set a strong POSTGRES_PASSWORD and user IDs:
   cp .env.example .env
   # edit /srv/mage_project/.env -> set POSTGRES_PASSWORD, UID, and GID
   # Get your user/group IDs: id -u (UID) and id -g (GID)
   chmod 600 /srv/mage_project/.env

Persistent storage & permissions
3) Prefer Docker named volumes (compose already configured). If you must use host folders, create them and set owner to container UID (recommended only for dev):
   sudo mkdir -p /srv/mage_project/pgdata /srv/mage_project/logs /srv/mage_project/downloads
   # find container UID (example used 999), then:
   sudo chown -R 999:999 /srv/mage_project/pgdata /srv/mage_project/logs /srv/mage_project/downloads
   sudo chmod 750 /srv/mage_project/pgdata /srv/mage_project/logs /srv/mage_project/downloads

Start services
4) Start stack with compose (from project root):
   cd /srv/mage_project
   sudo docker compose up -d --build

Verify
5) Check status and logs:
   sudo docker compose ps
   sudo docker compose logs -f mage
   sudo docker compose logs -f postgres

Backups & maintenance
6) Back up Postgres regularly (cron example):
   mkdir -p /srv/mage_project/backups
   # Example pg_dump (run on host or scheduled container):
   # First, create .pgpass file: echo "127.0.0.1:5432:indian_sm_dw:postgres:<PASSWORD>" > ~/.pgpass && chmod 600 ~/.pgpass
   pg_dump -h 127.0.0.1 -U postgres -F c -b -v -f /srv/mage_project/backups/magedb_$(date +%F).dump indian_sm_dw

Recommended backup strategy
- Regular full backups: schedule a daily pg_dump (custom format) and keep 7-30 rolling copies depending on retention policy. Example cron (daily at 02:00):
  0 2 * * * /usr/bin/pg_dump -h 127.0.0.1 -U $POSTGRES_USER -F c -b -v -f /srv/mage_project/backups/magedb_$(date +\%F).dump $POSTGRES_DB && find /srv/mage_project/backups -type f -mtime +30 -delete

- WAL shipping / continuous backup (for larger deployments): consider using pg_basebackup + WAL archiving or a managed backup tool.
- Offsite copies: periodically copy backups to remote storage (S3/rsync to another host) for disaster recovery.
- Test restores: at least weekly, restore a backup into a test DB to verify integrity.

Where Mage stores metadata & runtime artifacts
- Mage metadata (pipelines, run history, schedules, variables) is persisted in the metadata database when you set MAGE_DATABASE_URL (Postgres). Backing up the Postgres database is therefore sufficient to preserve Mage metadata.
- Note however: not everything is stored in Postgres. Project code, pipeline definitions, custom scripts, and some runtime artifacts (downloads, logs) live on the container filesystem or in mounted volumes:
  - Project code: in the project directory (e.g. /srv/mage_project) or the image if you didn't bind-mount. Back this up via git or file backups.
  - Logs and runtime downloads: if you use named volumes (mage-logs, app-downloads) back them up separately (e.g. copy to host or tar the volume contents).

Practical checklist before making changes that could affect data
- Create a Postgres dump and copy it off the host.
- Export or push your project repo to remote git.
- If using host bind mounts, ensure host folders are included in your backup scope.

Security & secrets
7) Do NOT commit .env. For production, use Docker secrets / a secret manager. Bind Postgres to localhost (compose uses 127.0.0.1:5432) and use firewall rules to restrict access.

Service management
8) Use docker compose (system service) or create a systemd unit calling `docker compose -f /srv/mage_project/docker-compose.yml up -d` to ensure auto start on reboot. Example systemd unit:

[Unit]
Description=Mage Compose Stack
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/srv/mage_project
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down

[Install]
WantedBy=multi-user.target

Upgrades
9) To upgrade code or image:
    git pull
    sudo docker compose up -d --build
    # For schema migrations, use the project's migration commands or run SQL via psql

Troubleshooting (quick)
- Postgres dns/connectivity: ensure both services are on same compose network (mage-net) and MAGE_DATABASE_URL uses host `mage-postgres`.
- Permission errors on bind mounts: either chown host dirs to container UID or switch to named volumes.
- Init SQL not running: init scripts run only when DB volume is empty; to re-run without losing data, run the SQL manually with psql inside the postgres container.

Contact / next steps
- Replace `<your-repo-url>` with your git origin. Update the doc with any site-specific firewall, SSL, or monitoring steps.
