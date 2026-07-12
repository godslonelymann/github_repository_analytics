import logging

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from database import get_engine


logger = logging.getLogger(__name__)


INSERT_REPOSITORY_SQL = text(
    """
    INSERT INTO repositories (
        repo_id,
        owner,
        repository_name,
        description,
        language,
        created_at,
        updated_at
    )
    VALUES (
        :repo_id,
        :owner,
        :repository_name,
        :description,
        :language,
        :created_at,
        :updated_at
    )
    ON CONFLICT (repo_id) DO NOTHING
    """
)

INSERT_METRICS_SQL = text(
    """
    INSERT INTO repository_metrics (
        repo_id,
        snapshot_date,
        stars,
        forks,
        watchers,
        open_issues
    )
    VALUES (
        :repo_id,
        :snapshot_date,
        :stars,
        :forks,
        :watchers,
        :open_issues
    )
    """
)


def load_repositories(repositories: list[dict], engine=None) -> None:
    engine = engine or get_engine()

    try:
        with engine.begin() as connection:
            for repository in repositories:
                connection.execute(INSERT_REPOSITORY_SQL, repository)
                connection.execute(INSERT_METRICS_SQL, repository)
    except SQLAlchemyError:
        logger.exception("PostgreSQL load failed")
        raise

    logger.info("Records inserted for %s repositories", len(repositories))
