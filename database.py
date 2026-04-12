from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://ayushmanbahinipati:@localhost:5432/notes_db"

engine = create_engine(DATABASE_URL)

sessionLocal = sessionmaker(autocommit = False, autoflush = False, bind=engine)

Base = declarative_base()