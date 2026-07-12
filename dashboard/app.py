import sys
from pathlib import Path

import streamlit as st
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from database import get_engine  # noqa: E402


st.set_page_config(page_title="GitHub Repository Analytics", layout="wide")
st.title("GitHub Repository Analytics")


@st.cache_data(ttl=300)
def fetch_dashboard_data():
    engine = get_engine()

    with engine.connect() as connection:
        summary = connection.execute(
            text(
                """
                SELECT
                    COUNT(DISTINCT r.repo_id) AS total_repositories,
                    COALESCE(SUM(latest.stars), 0) AS total_stars,
                    COALESCE(SUM(latest.forks), 0) AS total_forks
                FROM repositories r
                LEFT JOIN (
                    SELECT DISTINCT ON (repo_id)
                        repo_id,
                        stars,
                        forks
                    FROM repository_metrics
                    ORDER BY repo_id, snapshot_date DESC
                ) latest ON r.repo_id = latest.repo_id
                """
            )
        ).mappings().one()

        top_repositories = connection.execute(
            text(
                """
                SELECT
                    r.owner || '/' || r.repository_name AS repository,
                    latest.stars
                FROM repositories r
                JOIN (
                    SELECT DISTINCT ON (repo_id)
                        repo_id,
                        stars
                    FROM repository_metrics
                    ORDER BY repo_id, snapshot_date DESC
                ) latest ON r.repo_id = latest.repo_id
                ORDER BY latest.stars DESC
                LIMIT 10
                """
            )
        ).mappings().all()

        languages = connection.execute(
            text(
                """
                SELECT
                    COALESCE(language, 'Unknown') AS language,
                    COUNT(*) AS repository_count
                FROM repositories
                GROUP BY COALESCE(language, 'Unknown')
                ORDER BY repository_count DESC
                """
            )
        ).mappings().all()

        star_history = connection.execute(
            text(
                """
                SELECT
                    snapshot_date,
                    SUM(stars) AS total_stars
                FROM repository_metrics
                GROUP BY snapshot_date
                ORDER BY snapshot_date
                """
            )
        ).mappings().all()

    return {
        "summary": dict(summary),
        "top_repositories": [dict(row) for row in top_repositories],
        "languages": [dict(row) for row in languages],
        "star_history": [dict(row) for row in star_history],
    }


try:
    data = fetch_dashboard_data()
except SQLAlchemyError as exc:
    st.error(f"Could not connect to PostgreSQL: {exc}")
    st.stop()

summary = data["summary"]

metric_columns = st.columns(3)
metric_columns[0].metric("Total repositories", summary["total_repositories"])
metric_columns[1].metric("Total stars", summary["total_stars"])
metric_columns[2].metric("Total forks", summary["total_forks"])

st.subheader("Top repositories by stars")
st.bar_chart(data["top_repositories"], x="repository", y="stars")

st.subheader("Repository language distribution")
st.bar_chart(data["languages"], x="language", y="repository_count")

st.subheader("Star history over time")
st.line_chart(data["star_history"], x="snapshot_date", y="total_stars")
