import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database for the application
db_path = os.path.join(
    os.path.abspath(os.path.dirname(os.path.dirname(__file__))), "smartcam.sqlite"
)
engine = create_engine(f"sqlite:///{db_path}", echo=False)

# Base class for custom models
Base = declarative_base()

# Use factory pattern to create a new session
Session = sessionmaker(bind=engine)


def create_tables():
    print("Creating database tables...")
    Base.metadata.create_all(engine)
