# eSalama Infrastructure

This directory contains Docker Compose and other infrastructure configuration for the eSalama development environment.

## Docker Compose

`docker-compose.yml` starts the full development stack:

| Service      | Image / Build       | Port |
|-------------|---------------------|------|
| `db`         | postgres:15-alpine  | 5432 |
| `redis`      | redis:7-alpine      | 6379 |
| `backend`    | ./backend           | 8000 |
| `admin-portal` | ./admin-portal    | 3000 |

### Usage

From the **repository root**:

```bash
# Copy and (optionally) edit environment variables
cp .env.example .env

# Build and start all services
docker compose up --build

# Run in the background
docker compose up --build -d

# Stop all services
docker compose down

# Stop and remove volumes (resets the database)
docker compose down -v
```

Alternatively run directly from this directory (paths are relative to `infra/`):

```bash
cd infra
docker compose up --build
```

## Other Infrastructure

| Directory     | Purpose                          |
|--------------|----------------------------------|
| `kubernetes/` | Kubernetes manifests (planned)   |
| `monitoring/` | Prometheus / Grafana (planned)   |
| `nginx/`      | Reverse-proxy config (planned)   |
| `terraform/`  | Cloud provisioning (planned)     |
