from database.connection import engine
from database.base import Base

import models  # noqa: F401

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("DONE - tables created")