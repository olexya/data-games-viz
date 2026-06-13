# Data Games Viz

A working prototype of a **composable data platform**: an application to explore
statistics of [Steam](https://store.steampowered.com) games, built end-to-end with
[Kestra](https://kestra.io) (orchestration), [dbt](https://www.getdbt.com)
(transformation), [Evidence](https://evidence.dev) (visualization) and
[PostgreSQL](https://www.postgresql.org/) (storage).

> Companion open-source landscape (market study): https://github.com/olexya/oss-data-tools-landscape

The whole platform is deployed with a single `docker compose` command. Compose
orchestrates the full pipeline automatically:

`postgres` → `kestra` → `loader` (imports the flow, runs **get-data** then **dbt build**) → `evidence`

It follows a medallion architecture (Bronze → Silver → Gold). See
[docs/content.md](docs/content.md) for the architecture, UI guide and troubleshooting.

## Quick start

### Requirements
- Docker Engine 24.0+ and Docker Compose v2
- ~2 GB free disk space, internet access (image pulls + Steam API)

### Download
```sh
git clone https://github.com/olexya/data-games-viz.git
cd data-games-viz
```

### Launch

Using the helper scripts (recommended):

```sh
make up        # macOS / Linux
```
```powershell
.\make.ps1 up  # Windows (PowerShell)
```

…or directly with Docker Compose:
```sh
docker compose up -d
```

The initial setup may take 3-5 minutes (image pulls, Python/npm installs, first
Steam ingestion).

### Helper commands

| `make <target>` / `.\make.ps1 <target>` | Action                                        |
|-----------------------------------------|-----------------------------------------------|
| `up`                                    | Start the whole platform (detached)           |
| `down`                                  | Stop it (data preserved)                       |
| `restart`                               | Restart                                        |
| `reload`                                | Force a fresh Steam data reload                |
| `logs`                                  | Follow logs of all services                    |
| `ps`                                    | Container status                               |
| `clean`                                 | Stop **and** remove volumes + local data       |
| `urls`                                  | Print access URLs                              |

## Access

| Service    | URL                     | Notes                                            |
|------------|-------------------------|--------------------------------------------------|
| Evidence   | http://localhost:3000   | Dashboards                                        |
| Kestra     | http://localhost:8080   | Orchestrator UI/API — credentials below           |
| PostgreSQL | `localhost:5432`        | Host port configurable via `POSTGRES_HOST_PORT`   |

Kestra 1.x requires authentication. Default credentials (configurable in `.env`):
`admin@kestra.io` / `Kestra1234!` — **change them before any real use**.

## Configuration (`.env`)
- `POSTGRES_HOST_PORT` — host port for PostgreSQL (default `5432`; override to avoid conflicts).
- `KESTRA_BASIC_AUTH_USERNAME` / `KESTRA_BASIC_AUTH_PASSWORD` — Kestra login (the password must meet complexity: upper/lower/digit/symbol).
- `KESTRA_TENANT` — Kestra API tenant (default `main`).
- `NUMBER_APP` — optional, number of Steam apps ingested by a run (defaults to the flow's value, 190). Set a small value for a fast run.
- `RELOAD_MAX_AGE_HOURS` — data is reloaded only if the last successful load is older than this (default `24`). A `docker compose up` with fresh data **skips** ingestion (no needless Steam re-download).
- `FORCE_RELOAD=true` — force a reload regardless of freshness (or use `make reload`).

To customize Compose locally without touching the committed file, create a
`docker-compose.override.yml` (git-ignored), e.g. to remap the PostgreSQL host
port or set `NUMBER_APP`.

## Component versions
PostgreSQL **18** · Kestra **1.3.22** · Python **3.13** (loader) · dbt (postgres) · Evidence.

## Cross-platform
Internal services communicate over the named Docker network `data-games-viz`
(Kestra task containers join it via `networkMode`), so the stack runs on
macOS, Windows and Linux without relying on `host.docker.internal`.

## Credit
Special thanks to [Kestra](https://kestra.io), [dbt](https://www.getdbt.com),
[Evidence](https://evidence.dev) and [PostgreSQL](https://www.postgresql.org/)
for their contributions to this project.
