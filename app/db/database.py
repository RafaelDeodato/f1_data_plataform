from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.settings import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

engine = create_engine(
    settings.database_url,
    echo=False,
    pool_pre_ping=True
)

Sessionlocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    logger.info("Creating database session")
    return Sessionlocal()
