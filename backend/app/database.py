from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///projet-api-ecotrack.db")

Sessionmaker = sessionmaker(engine)
