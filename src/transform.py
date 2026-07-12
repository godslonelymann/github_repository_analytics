import logging
from datetime import date, datetime


logger = logging.getLogger(__name__)


REQUIRED_FIELDS = [
    "id",
    "name",
    "owner",
    "stargazers_count",
    "forks_count",
    "watchers_count",
    "open_issues_count",
    "created_at",
    "updated_at",
]


def _parse_github_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def transform_repository(repository: dict, snapshot_date: date | None = None) -> dict:
    missing_fields = [field for field in REQUIRED_FIELDS if field not in repository]
    if missing_fields:
        raise ValueError(f"Repository payload is missing fields: {', '.join(missing_fields)}")

    owner = repository["owner"]
    if not isinstance(owner, dict) or not owner.get("login"):
        raise ValueError("Repository payload is missing owner login")

    created_at = _parse_github_datetime(repository["created_at"])
    updated_at = _parse_github_datetime(repository["updated_at"])
    snapshot = snapshot_date or date.today()

    return {
        "repo_id": int(repository["id"]),
        "owner": owner["login"],
        "repository_name": repository["name"],
        "description": repository.get("description"),
        "language": repository.get("language"),
        "created_at": created_at,
        "updated_at": updated_at,
        "snapshot_date": snapshot,
        "stars": int(repository["stargazers_count"]),
        "forks": int(repository["forks_count"]),
        "watchers": int(repository["watchers_count"]),
        "open_issues": int(repository["open_issues_count"]),
    }


def transform_repositories(repositories: list[dict], snapshot_date: date | None = None) -> list[dict]:
    transformed = [transform_repository(repository, snapshot_date) for repository in repositories]
    logger.info("Data transformed for %s repositories", len(transformed))
    return transformed
