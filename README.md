# GitHub Repository Analytics ETL Pipeline

A simple Python ETL pipeline that fetches GitHub repository data from the GitHub REST API, transforms it into a small analytics shape, loads it into PostgreSQL, and displays basic trends in Streamlit.

The pipeline can run manually with `python run_pipeline.py` or on a daily Airflow schedule.

## Extra Documentation

- [README_CODEBASE.md](README_CODEBASE.md): explains every important file in simple language, with diagrams and flowcharts.
- [README_RUN.md](README_RUN.md): explains how to run the project step by step in simple language.

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

## Technologies Used

- Python 3.10+
- PostgreSQL
- SQLAlchemy
- Requests
- Psycopg2
- Streamlit
- Pytest
- Apache Airflow

## Folder Structure

```text
github-repository-analytics/
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── run_pipeline.py
│   ├── database.py
│   └── config.py
├── dashboard/
│   └── app.py
├── dags/
│   └── github_repo_analytics_dag.py
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── sql/
│   └── schema.sql
├── tests/
├── requirements.txt
├── requirements-airflow.txt
├── README.md
├── README_CODEBASE.md
├── README_RUN.md
├── run_pipeline.py
└── .env.example
```

`run_pipeline.py` at the project root is a small convenience entry point so the pipeline can be started with `python run_pipeline.py`.

## PostgreSQL Setup

Create the local database:

```bash
createdb github_analytics
```

Create the tables:

```bash
psql -d github_analytics -f sql/schema.sql
```

The schema creates two tables:

- `repositories`: static repository details, inserted only once per repository. Columns: `repo_id`, `owner`, `repository_name`, `description`, `language`, `created_at`, `updated_at`.
- `repository_metrics`: daily metric snapshots, inserted on every pipeline run.

## GitHub Token

A GitHub Personal Access Token is optional for public repositories, but recommended to avoid low API rate limits.

Create a token in GitHub, then create a `.env` file in the project folder:

```text
GITHUB_TOKEN=your_token_here
```

No special repository permissions are required for public repository metadata.

The project reads `.env` automatically. Do not commit `.env` to GitHub.

## Environment Variables

By default, the app connects to a local PostgreSQL database named `github_analytics` using the current OS user over the local PostgreSQL socket:

```text
postgresql+psycopg2:///github_analytics
```

Set environment variables only if your PostgreSQL installation needs a host, username, or password:

```bash
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_DB=github_analytics
export POSTGRES_USER=your_postgres_user
export POSTGRES_PASSWORD=your_postgres_password
```

You can also provide one full SQLAlchemy connection string:

```bash
export DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/github_analytics
```

## Install Dependencies

```bash
python -m pip install -r requirements.txt
```

If your system uses `python3` instead of `python`, use `python3` for the commands below.

## Run the Pipeline

```bash
python run_pipeline.py
```

The pipeline fetches the 100 repositories listed in `src/config.py`, transforms the API responses, inserts new repositories if needed, and appends metric snapshots.

## Run with Docker

The Docker setup uses four simple services:

```text
postgres   -> PostgreSQL database
etl        -> manual ETL runner
dashboard  -> Streamlit dashboard
airflow    -> Airflow scheduler and web UI
```

The Docker PostgreSQL credentials are:

```text
database: github_analytics
username: postgres
password: postgres
```

Build the image:

```bash
docker compose build
```

Start PostgreSQL:

```bash
docker compose up -d postgres
```

Run the ETL manually:

```bash
docker compose run --rm etl
```

Start the dashboard:

```bash
docker compose up dashboard
```

Open:

```text
http://localhost:8501
```

Start Airflow:

```bash
docker compose up airflow
```

Open:

```text
http://localhost:8080
```

Login:

```text
username: admin
password: admin
```

Enable the `github_repo_analytics_etl` DAG in the Airflow UI.

To stop all Docker services:

```bash
docker compose down
```

## Run with Airflow

The Airflow integration is intentionally simple. The DAG runs the existing pipeline script once per day:

```text
dags/github_repo_analytics_dag.py
    |
    v
python run_pipeline.py
```

Install Airflow in the same environment where the project dependencies are available:

```bash
python -m pip install -r requirements.txt
python -m pip install -r requirements-airflow.txt
```

Set Airflow home and point Airflow at this project's `dags/` folder:

```bash
export AIRFLOW_HOME="$PWD/airflow_home"
export AIRFLOW__CORE__DAGS_FOLDER="$PWD/dags"
```

Start Airflow:

```bash
airflow standalone
```

Airflow will print the admin username and password in the terminal. Open the Airflow UI:

```text
http://localhost:8080
```

Enable the `github_repo_analytics_etl` DAG. It uses `start_date=datetime(2026, 7, 12)`, `schedule="@daily"`, and `catchup=False`, so it will not backfill old dates.

## Verify PostgreSQL Data

```bash
psql -d github_analytics
```

Then run:

```sql
SELECT COUNT(*) FROM repositories;
SELECT COUNT(*) FROM repository_metrics;

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

## Run the Dashboard

```bash
streamlit run dashboard/app.py
```

The dashboard shows:

- Total repositories
- Total stars
- Total forks
- Top repositories by stars
- Repository language distribution
- Star history over time

## Run Tests

```bash
pytest tests
```

The tests cover repository transformation, database insertion calls, and a complete ETL orchestration using sample data.
