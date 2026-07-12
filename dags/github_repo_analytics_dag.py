import shlex
import sys
from datetime import datetime
from pathlib import Path

from airflow import DAG
from airflow.operators.bash import BashOperator


PROJECT_ROOT = Path(__file__).resolve().parents[1]


with DAG(
    dag_id="github_repo_analytics_etl",
    description="Run the GitHub repository analytics ETL pipeline.",
    start_date=datetime(2026, 7, 12),
    schedule="@daily",
    catchup=False,
    tags=["github", "etl"],
) as dag:
    run_pipeline = BashOperator(
        task_id="run_pipeline",
        bash_command=(
            f"cd {shlex.quote(str(PROJECT_ROOT))} "
            f"&& {shlex.quote(sys.executable)} run_pipeline.py"
        ),
    )
