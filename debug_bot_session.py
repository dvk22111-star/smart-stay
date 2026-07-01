from database.connection import engine
from database.base import Base
from models import BotRegistrationSession
from sqlalchemy.orm import Session
import traceback

try:
    with Session(engine) as session:
        new_session = BotRegistrationSession(
            Phone='0501234567',
            VacationID=1,
            GroupID=None,
            Status='AWAITING_VERIFICATION'
        )
        session.add(new_session)
        session.commit()
        print(f'Success! SessionID: {new_session.SessionID}')
except Exception as e:
    print(f'Error: {e}')
    traceback.print_exc()
