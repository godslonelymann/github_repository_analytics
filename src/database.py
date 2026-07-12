import logging

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

from config import DATABASE_URL


logger = logging.getLogger(__name__)


def get_engine(database_url: str = DATABASE_URL):
    try:
        return create_engine(database_url, pool_pre_ping=True)
    except SQLAlchemyError:
        logger.exception("PostgreSQL connection setup failed")
        raise
