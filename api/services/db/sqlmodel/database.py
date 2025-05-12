import contextlib
import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session, SQLModel


load_dotenv()

POSTGRES_URI = os.getenv("POSTGRES_URI")

engine = create_engine(POSTGRES_URI, echo=True)

def get_session():
    with Session(engine) as session:
        yield session


def reset_database():
    meta = SQLModel.metadata

    with contextlib.closing(engine.connect()) as con:
        trans = con.begin()
        for table in reversed(meta.sorted_tables):
            con.execute(table.delete())
        trans.commit()

    return
