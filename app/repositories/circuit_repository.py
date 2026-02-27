from app.db.database import get_db
from app.db.models.circuit import Circuit

class CircuitRepository:
    def __init__(self):
        self.db = get_db()

    def add_circuit(self, circuit_data: dict):
        new_circuit = Circuit(
                circuit_id=circuit_data['circuitId'],
                wikipedia_url=circuit_data['url'],
                name=circuit_data['circuitName'],
                loc_latitude=circuit_data['Location']['lat'],
                loc_longitude=circuit_data['Location']['long'],
                loc_locality=circuit_data['Location']['locality'],
                loc_country=circuit_data['Location']['country']
            )   

        self.db.add(new_circuit) 
        self.db.commit()
        self.db.refresh(new_circuit)
        return new_circuit
    
    def close(self):
        self.db.close()