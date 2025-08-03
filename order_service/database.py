from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from common.configurations import config
DATABASE_URL = config['DB']['order.url']

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()

    try: 
        yield db
    finally:
        db.close()
        