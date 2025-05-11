import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session, SQLModel


load_dotenv()

POSTGRES_URI = os.getenv("POSTGRES_URI")

engine = create_engine(POSTGRES_URI, echo=True)
SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


def reset_database():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    return
