import os
from pathlib import Path


def load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return

    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        os.environ.setdefault(key, value)


load_env_file(Path(__file__).resolve().parents[1] / ".env")


GITHUB_API_BASE_URL = "https://api.github.com"

REPOSITORIES = [
    "python/cpython",
    "pallets/flask",
    "django/django",
    "psf/requests",
    "fastapi/fastapi",
    "sqlalchemy/sqlalchemy",
    "pytest-dev/pytest",
    "pandas-dev/pandas",
    "numpy/numpy",
    "scikit-learn/scikit-learn",
    "streamlit/streamlit",
    "apache/airflow",
    "docker/compose",
    "kubernetes/kubernetes",
    "facebook/react",
    "vuejs/core",
    "angular/angular",
    "nodejs/node",
    "microsoft/vscode",
    "torvalds/linux",
    "ansible/ansible",
    "tensorflow/tensorflow",
    "pytorch/pytorch",
    "keras-team/keras",
    "huggingface/transformers",
    "langchain-ai/langchain",
    "openai/openai-python",
    "tiangolo/typer",
    "encode/httpx",
    "encode/django-rest-framework",
    "celery/celery",
    "scrapy/scrapy",
    "jupyter/notebook",
    "jupyterlab/jupyterlab",
    "ipython/ipython",
    "matplotlib/matplotlib",
    "plotly/plotly.py",
    "apache/superset",
    "apache/spark",
    "apache/kafka",
    "apache/flink",
    "dbt-labs/dbt-core",
    "PrefectHQ/prefect",
    "dagster-io/dagster",
    "great-expectations/great_expectations",
    "apache/beam",
    "elastic/elasticsearch",
    "redis/redis",
    "mongodb/mongo",
    "postgres/postgres",
    "mysql/mysql-server",
    "ClickHouse/ClickHouse",
    "duckdb/duckdb",
    "trinodb/trino",
    "grafana/grafana",
    "prometheus/prometheus",
    "hashicorp/terraform",
    "hashicorp/vault",
    "hashicorp/consul",
    "helm/helm",
    "istio/istio",
    "envoyproxy/envoy",
    "gohugoio/hugo",
    "gin-gonic/gin",
    "gorilla/mux",
    "golang/go",
    "rust-lang/rust",
    "denoland/deno",
    "vercel/next.js",
    "sveltejs/svelte",
    "vitejs/vite",
    "webpack/webpack",
    "babel/babel",
    "eslint/eslint",
    "prettier/prettier",
    "tailwindlabs/tailwindcss",
    "nestjs/nest",
    "expressjs/express",
    "typeorm/typeorm",
    "prisma/prisma",
    "reduxjs/redux",
    "reduxjs/redux-toolkit",
    "storybookjs/storybook",
    "mui/material-ui",
    "ant-design/ant-design",
    "twbs/bootstrap",
    "jquery/jquery",
    "laravel/laravel",
    "symfony/symfony",
    "rails/rails",
    "rubygems/rubygems",
    "jekyll/jekyll",
    "Homebrew/brew",
    "swiftlang/swift",
    "electron/electron",
    "flutter/flutter",
    "dart-lang/sdk",
    "JetBrains/kotlin",
    "spring-projects/spring-boot",
    "spring-projects/spring-framework",
]

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "github_analytics")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    if POSTGRES_HOST:
        credentials = ""
        if POSTGRES_USER and POSTGRES_PASSWORD:
            credentials = f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
        elif POSTGRES_USER:
            credentials = f"{POSTGRES_USER}@"

        DATABASE_URL = (
            f"postgresql+psycopg2://{credentials}"
            f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
        )
    else:
        DATABASE_URL = f"postgresql+psycopg2:///{POSTGRES_DB}"
