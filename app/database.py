from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from os import getenv

load_dotenv()
USER = getenv('USER')
PASSWORD = getenv('PASSWORD')
DATABASE = getenv('DATABASE')

DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@localhost/{DATABASE}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
