import logging

from config import REPOSITORIES
from extract import extract_repositories
from load import load_repositories
from transform import transform_repositories


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


def run_pipeline(repositories: list[str] | None = None) -> list[dict]:
    logger.info("Pipeline started")
    repository_list = repositories or REPOSITORIES
    raw_repositories = extract_repositories(repository_list)
    transformed_repositories = transform_repositories(raw_repositories)
    load_repositories(transformed_repositories)
    logger.info("Pipeline completed")
    return transformed_repositories


if __name__ == "__main__":
    run_pipeline()
