from app.core.settings import settings
from app.core.logger import setup_logger, get_logger
from app.clients.jolpica_client import JolpicaClient
from app.db.database import get_db
from app.db.models.season import Season
from app.repositories.season_repository import SeasonRepository

def main():
    setup_logger()
    logger = get_logger(__name__)

    logger.info("Starting ingestion of historical seasons")
    logger.info(f"Current environment: {settings.ENV}")

    try:
        client = JolpicaClient()
        season_data = client.get_all_seasons()

        season_repository = SeasonRepository()

        for season in season_data:
            season_repository.add_season(season)
            logger.info(f"Inserted season {season['season']} into the database")

        season_repository.close()

    except Exception as e:
        logger.error(f"An error occurred: {e}")

    logger.info("Historical seasons ingestion completed successfully")


if __name__ == "__main__":    
    main()