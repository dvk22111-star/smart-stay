import sys
import sqlite3
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from database.base import Base
from models import BotRegistrationSession

# Setup SQLite with foreign keys enabled
engine = create_engine("sqlite:///smart_stay.db", echo=True)

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

try:
    with Session(engine) as session:
        new_session = BotRegistrationSession(
            Phone='0501234567',
            VacationID=1,
            GroupID=1,  # This doesn't exist!
            Status='AWAITING_VERIFICATION'
        )
        session.add(new_session)
        session.commit()
        print(f'Success! SessionID: {new_session.SessionID}')
except Exception as e:
    print(f'Error: {e}')
    print(f'Type: {type(e).__name__}')
    import traceback
    traceback.print_exc()
