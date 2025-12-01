from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends

DB_URL = "sqlite:///car_plates.db"
engine = create_engine(DB_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]


     