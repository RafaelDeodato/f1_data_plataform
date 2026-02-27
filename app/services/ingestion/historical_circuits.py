from app.core.settings import settings
from app.core.logger import setup_logger, get_logger
from app.clients.jolpica_client import JolpicaClient
from app.db.database import get_db
from app.db.models.circuit import Circuit
from app.repositories.circuit_repository import CircuitRepository

def main():
    setup_logger()
    logger = get_logger(__name__)

    logger.info("Starting ingestion of historical circuits")
    logger.info(f"Current environment: {settings.ENV}")

    try:
        client = JolpicaClient()
        circuit_data = client.get_all_circuits()

        circuit_repository = CircuitRepository()

        for circuit in circuit_data:
            circuit_repository.add_circuit(circuit)
            logger.info(f"Inserted circuit {circuit['circuitName']} into the database")
            
        circuit_repository.close()

    except Exception as e:
        logger.error(f"An error occurred: {e}")

    logger.info("Historical circuits ingestion completed successfully")

if __name__ == "__main__":    
    main()