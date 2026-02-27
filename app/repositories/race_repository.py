from app.db.database import get_db
from app.db.models.race import Race

class RaceRepository:
    def __init__(self):
        self.db = get_db()

    def add_race(self, race_data: dict, season_year: int):
        new_race =  Race(
            season=season_year,
            round=race_data['round'],
            wikipedia_url=race_data['url'],
            name=race_data['raceName'],
            #official_name=official_name,
            circuit_id=race_data['Circuit']['circuitId'],
            date=race_data['date'],
            time=race_data.get('time', None),
            #meeting_key_openf1=meeting_key_openf1
        )
        self.db.add(new_race)
        self.db.commit()
        self.db.refresh(new_race)
        return new_race
    
    def get_race_id(self, season_year: int, round_number: int):
        return self.db.query(Race).filter_by(season=season_year, round=round_number).first().id
    
    def get_race(self, season_year: int, round_number: int):
        return self.db.query(Race).filter_by(season=season_year, round=round_number).first()

    def update_openf1_data(self, season_year: int, round_number: int, official_name: str, meeting_key: int):
        race = self.get_race(season_year, round_number)
        race.official_name = official_name
        race.meeting_key_openf1 = meeting_key
        self.db.commit()
        self.db.refresh(race)
        return race

    def close(self):
        self.db.close()