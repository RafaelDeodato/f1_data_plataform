from app.core.settings import settings
from app.core.logger import setup_logger, get_logger
from app.clients.jolpica_client import JolpicaClient
from app.clients.openf1_client import OpenF1Client
from app.db.database import get_db
from app.db.models import session
from app.repositories.session_repository import SessionRepository
from app.repositories.race_repository import RaceRepository
from app.repositories.season_repository import SeasonRepository

def match_openf1_event(jolpica_race, openf1_meetings):
    for meeting in openf1_meetings:
        if meeting['meeting_name'] == jolpica_race['raceName']:
            return meeting
        
def match_openf1_session(session_type, openf1_sessions):
    session_openf1_name_map = {
        "FP1": "Practice 1",
        "FP2": "Practice 2",
        "FP3": "Practice 3",
        "Q": "Qualifying",
        "Sprint": "Sprint",
        "SQ": "Sprint Shootout"
    }

    if session_type not in session_openf1_name_map:
        return None

    openf1_session_name = session_openf1_name_map[session_type]

    for session in openf1_sessions:
        if session.get("session_name") == openf1_session_name:
            return session

    return None

def main():
    setup_logger()
    logger = get_logger(__name__)

    logger.info("Starting ingestion of historical races and sessions")
    logger.info(f"Current environment: {settings.ENV}")

    session_map = {
        "FirstPractice": "FP1",
        "SecondPractice": "FP2",
        "ThirdPractice": "FP3",
        "Qualifying": "Q",
        "Sprint": "Sprint",
        "SprintShootout": "SQ",
    }

    try:
        client_jolpica = JolpicaClient()
        client_openf1 = OpenF1Client()
        season_repository = SeasonRepository()
        race_repository = RaceRepository()
        session_repository = SessionRepository()

        seasons = season_repository.get_all_seasons()

        for season in seasons:
            year = season.year

            if year < 2025:
                logger.info(f"Skipping season {year} as it is before 2025")
                continue

            races = client_jolpica.get_all_races(year=year)
            logger.info(f"Found {len(races)} races for season {year}. On Jolpica API")

            meetings_openf1 = client_openf1.get_meetings_by_season(year)
            logger.info(f"Found {len(meetings_openf1)} meetings for season {year}. On OpenF1 API")

            for race in races:
                race_db = race_repository.add_race(race, year)
                logger.info(f"Inserted race {race_db.name} into the database")
                race_id = race_db.id

                openf1_event = match_openf1_event(race, meetings_openf1)
                if openf1_event:
                    official_name = openf1_event['meeting_official_name'] if openf1_event['meeting_official_name'] else None
                    meeting_key_openf1 = openf1_event['meeting_key']

                    race_repository.update_openf1_data(year, race['round'], official_name, meeting_key_openf1)
                    logger.info(f"Updated race {race_db.name} with OpenF1 data: official_name={official_name}, meeting_key_openf1={meeting_key_openf1}")
                elif openf1_event is None:
                    logger.warning(f"No matching OpenF1 event found for race {race['raceName']} in season {year}")
                    
                if openf1_event:
                    openf1_sessions = client_openf1.get_sessions_by_meeting(meeting_key_openf1)
                    logger.info(f"Found {len(openf1_sessions)} sessions for meeting {meeting_key_openf1} (race {race['raceName']}) in season {year}. On OpenF1 API")
                else:
                    openf1_sessions = []
                    logger.warning(f"Skipping fetching sessions from OpenF1 API for race {race['raceName']} in season {year} as no matching event was found")

                for key, session_type in session_map.items():
                    if key in race:
                        session_info = race[key]
                        session_repository.add_session(session_info, race_id, key, session_type)
                        logger.info(f"Inserted session {session_type} for race {race_db.name} into the database")

                        if openf1_sessions:
                            openf1_session = match_openf1_session(session_type, openf1_sessions)
                            if openf1_session:
                                session_repository.update_session_with_openf1_data(race_id, key, openf1_session['session_key'])
                                logger.info(f"Updated session {session_type} for race {race_db.name} with OpenF1 data: session_key={openf1_session['session_key']}")
                            elif openf1_session is None:
                                logger.warning(f"No matching OpenF1 session found for session {session_type} of race {race['raceName']} in season {year}")
                        else:
                            logger.warning(f"Skipping matching OpenF1 session for session {session_type} of race {race['raceName']} in season {year} as no OpenF1 sessions were available")

    except Exception:
        logger.exception("An error occurred during the ingestion of historical races and sessions")
        raise
    logger.info("Historical races and sessions ingestion completed successfully")

if __name__ == "__main__":    
    main()