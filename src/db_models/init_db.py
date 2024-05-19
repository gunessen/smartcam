from .base import Base, engine


def create_tables():
    print("Creating database tables...")
    Base.metadata.create_all(engine)
