# GitHub Repository Analytics ETL Pipeline

A Python data engineering project that extracts public GitHub repository metadata, transforms it into an analytics-friendly shape, stores daily metric snapshots in PostgreSQL, and visualizes the results in Streamlit.

The project is designed to be easy to run locally, in Docker, or on a daily Apache Airflow schedule.

## What It Does

- Tracks a curated list of 100 popular open source repositories.
- Pulls repository metadata from the GitHub REST API.
- Captures daily snapshots for stars, forks, watchers, and open issues.
- Stores stable repository attributes and historical metrics in PostgreSQL.
- Provides a Streamlit dashboard for repository totals, top repositories, language distribution, and star history.
- Includes pytest coverage for transformation, loading, and orchestration logic.

## Dashboard Screenshots

### Repository Summary and Top Repositories

![Repository summary and top repositories](dashboard/dashboard-ss/img-1.png)

The dashboard summary cards show the total number of tracked repositories, total stars, and total forks loaded into PostgreSQL. The bar chart ranks the top repositories by their latest star count, making it easy to compare the highest-impact repositories in the dataset.

### Repository Language Distribution

![Repository language distribution](dashboard/dashboard-ss/img-2.png)

This chart groups repositories by their primary GitHub language. It helps show the technology mix across the tracked repositories, with Python, TypeScript, Go, JavaScript, Java, and other languages represented in the current dataset.

### Star History Over Time

![Star history over time](dashboard/dashboard-ss/img-3.png)

The star history chart uses the accumulated records in `repository_metrics` to show how total stars change across ETL snapshots. Each pipeline run adds a new snapshot, so this view becomes more useful as the scheduled Airflow job or manual ETL runs collect more history.

## Architecture

```text
GitHub REST API
      |
      v
src/extract.py
      |
      v
src/transform.py
      |
      v
src/load.py
      |
      v
PostgreSQL
      |
      v
dashboard/app.py
```

Airflow schedules the same pipeline entry point used for manual runs:

```text
dags/github_repo_analytics_dag.py -> python run_pipeline.py
```

## Tech Stack

- Python 3.10+
- PostgreSQL
- SQLAlchemy
- Requests
- Streamlit
- Pytest
- Apache Airflow
- Docker and Docker Compose

## Repository Structure

```text
.
├── dags/
│   └── github_repo_analytics_dag.py
├── dashboard/
│   ├── dashboard-ss/
│   │   ├── img-1.png
│   │   ├── img-2.png
│   │   └── img-3.png
│   └── app.py
├── sql/
│   └── schema.sql
├── src/
│   ├── config.py
│   ├── database.py
│   ├── extract.py
│   ├── load.py
│   ├── run_pipeline.py
│   └── transform.py
├── tests/
│   ├── conftest.py
│   ├── test_load.py
│   ├── test_run_pipeline.py
│   └── test_transform.py
├── Dockerfile
├── docker-compose.yml
├── requirements-airflow.txt
├── requirements.txt
└── run_pipeline.py
```

The root `run_pipeline.py` is a convenience wrapper that loads and runs `src/run_pipeline.py`.

## Data Model

The PostgreSQL schema contains two tables:

| Table | Purpose |
| --- | --- |
| `repositories` | Stores stable repository metadata such as repository ID, owner, name, description, language, creation time, and last update time. |
| `repository_metrics` | Stores a new metric snapshot on every pipeline run, including stars, forks, watchers, open issues, and snapshot date. |

`repositories.repo_id` is the primary key. Repository rows are inserted once with `ON CONFLICT DO NOTHING`; metric rows are appended each time the ETL runs.

## Configuration

The project reads environment variables directly and also loads a local `.env` file from the project root when present.

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `GITHUB_TOKEN` | No | Empty | Optional GitHub token. Recommended to avoid low unauthenticated API rate limits. |
| `DATABASE_URL` | No | Built from PostgreSQL variables | Full SQLAlchemy PostgreSQL connection string. Takes precedence over individual PostgreSQL settings. |
| `POSTGRES_HOST` | No | Empty | PostgreSQL host. If omitted, the app uses a local socket URL. |
| `POSTGRES_PORT` | No | `5432` | PostgreSQL port. |
| `POSTGRES_DB` | No | `github_analytics` | PostgreSQL database name. |
| `POSTGRES_USER` | No | Empty | PostgreSQL username. |
| `POSTGRES_PASSWORD` | No | Empty | PostgreSQL password. |

Example `.env`:

```text
GITHUB_TOKEN=your_github_token
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=github_analytics
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

You can also use one complete connection string:

```text
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/github_analytics
```

Do not commit `.env` files or real secrets.

## Quick Start with Docker

Docker Compose runs PostgreSQL, the ETL job, Streamlit, and Airflow with consistent container settings.

Build the image:

```bash
docker compose build
```

Start PostgreSQL:

```bash
docker compose up -d postgres
```

Run the ETL pipeline:

```bash
docker compose run --rm etl
```

Start the dashboard:

```bash
docker compose up dashboard
```

Open the dashboard at:

```text
http://localhost:8501
```

Stop services:

```bash
docker compose down
```

Remove services and delete the PostgreSQL volume:

```bash
docker compose down -v
```

Use `-v` only when you intentionally want to delete the local Docker database.

## Local Development Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Create the PostgreSQL database:

```bash
createdb github_analytics
```

Create the tables:

```bash
psql -d github_analytics -f sql/schema.sql
```

Run the pipeline:

```bash
python run_pipeline.py
```

Run the dashboard:

```bash
streamlit run dashboard/app.py
```

## Running with Airflow

Airflow is optional for scheduled execution.

Install the application and Airflow dependencies:

```bash
python -m pip install -r requirements.txt
python -m pip install -r requirements-airflow.txt
```

Set Airflow paths for this project:

```bash
export AIRFLOW_HOME="$PWD/airflow_home"
export AIRFLOW__CORE__DAGS_FOLDER="$PWD/dags"
```

Start Airflow:

```bash
airflow standalone
```

Open:

```text
http://localhost:8080
```

Enable the `github_repo_analytics_etl` DAG. The DAG is configured with:

- `schedule="@daily"`
- `catchup=False`
- `start_date=datetime(2026, 7, 12)`

The Docker Compose Airflow service creates an admin user automatically:

```text
Username: admin
Password: admin
```

## Testing

Run the test suite:

```bash
pytest tests
```

Current tests cover:

- Repository payload transformation.
- Validation of missing required fields.
- Loader execution against a fake SQLAlchemy engine.
- End-to-end pipeline orchestration with mocked extract, transform, and load steps.

## Useful SQL Checks

After a successful ETL run:

```sql
SELECT COUNT(*) FROM repositories;
SELECT COUNT(*) FROM repository_metrics;
```

View the latest high-star repositories:

```sql
SELECT
    r.owner,
    r.repository_name,
    m.snapshot_date,
    m.stars,
    m.forks,
    m.watchers,
    m.open_issues
FROM repositories r
JOIN repository_metrics m ON r.repo_id = m.repo_id
ORDER BY m.snapshot_date DESC, m.stars DESC
LIMIT 10;
```

## Operational Notes

- The repository list is defined in `src/config.py`.
- Public GitHub metadata can be fetched without a token, but authenticated requests are more reliable for repeated runs.
- Docker initializes `sql/schema.sql` only when the PostgreSQL volume is first created.
- Local runs default to `postgresql+psycopg2:///github_analytics` when `POSTGRES_HOST` and `DATABASE_URL` are not set.
- The dashboard uses the latest metrics per repository for summary cards and top repository rankings.
- Historical star trends are based on accumulated rows in `repository_metrics`.

## Troubleshooting

### GitHub API Rate Limits

Set `GITHUB_TOKEN` in `.env` or in your shell environment.

### Local PostgreSQL Connection Errors

If your PostgreSQL server requires explicit credentials, set either `DATABASE_URL` or the individual `POSTGRES_*` variables.

### Docker Port Conflicts

The Compose file exposes:

| Service | Port |
| --- | --- |
| PostgreSQL | `5432` |
| Streamlit | `8501` |
| Airflow | `8080` |

Stop the conflicting process or update `docker-compose.yml` to use a different host port.

### Schema Changes Not Appearing in Docker

The schema file runs only during first-time PostgreSQL volume initialization. Recreate the database volume if you want Docker to apply schema changes from scratch:

```bash
docker compose down -v
docker compose up -d postgres
```
