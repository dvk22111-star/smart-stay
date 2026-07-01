from database.base import Base
from database.connection import engine

import models

try:
    Base.metadata.create_all(bind=engine)
    print("SUCCESS")
except Exception as e:
    print(e)