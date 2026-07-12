import logging
import time

import requests

from config import GITHUB_API_BASE_URL, GITHUB_TOKEN


logger = logging.getLogger(__name__)


def fetch_repository(owner: str, repository_name: str, retries: int = 3, timeout: int = 15) -> dict:
    url = f"{GITHUB_API_BASE_URL}/repos/{owner}/{repository_name}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "github-repository-analytics-etl",
    }

    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    last_error = None
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.JSONDecodeError as exc:
            logger.error("Invalid JSON received for %s/%s", owner, repository_name)
            raise ValueError(f"Invalid JSON received for {owner}/{repository_name}") from exc
        except requests.RequestException as exc:
            last_error = exc
            logger.warning(
                "GitHub API request failed for %s/%s on attempt %s/%s",
                owner,
                repository_name,
                attempt,
                retries,
            )
            if attempt < retries:
                time.sleep(attempt)

    raise RuntimeError(f"GitHub API request failed for {owner}/{repository_name}") from last_error


def extract_repositories(repositories: list[str]) -> list[dict]:
    extracted = []
    for repository in repositories:
        owner, repository_name = repository.split("/", 1)
        extracted.append(fetch_repository(owner, repository_name))

    logger.info("API requests completed for %s repositories", len(extracted))
    return extracted
