from app.db.database import get_db
from app.db.models.session import Session

class SessionRepository:
    def __init__(self):
        self.db = get_db()

    def add_session(self, session_data: dict, race_id: int, session_name: str, session_type: str):
        new_session = Session(
            #id=session_data['sessionId'],
            race_id=race_id,
            type=session_type,
            name=session_name,
            date=session_data['date'],
            time=session_data.get('time', None)
        )
        self.db.add(new_session)
        self.db.commit()
        self.db.refresh(new_session)
        return new_session
    
    def update_session_with_openf1_data(self, race_id: int, session_name: str, session_key_openf1: int):
        session = self.db.query(Session).filter_by(race_id=race_id, name=session_name).first()
        if session: 
            session.session_key_openf1 = session_key_openf1
            self.db.commit()
            self.db.refresh(session)
            return session
    
    def close(self):
        self.db.close()