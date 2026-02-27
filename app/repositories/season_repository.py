from app.db.database import get_db
from app.db.models.season import Season

class SeasonRepository:
    def __init__(self):
        self.db = get_db()

    def add_season(self, season_data: dict):
        new_season = Season(
            year=season_data['season'],
            wikipedia_url=season_data['url']
        )

        self.db.add(new_season)
        self.db.commit()
        self.db.refresh(new_season)
        return new_season
    
    def get_all_seasons(self):
        return self.db.query(Season).all()
    
    def close(self):
        self.db.close()