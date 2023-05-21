from duo.depends.depends_engine import get_engine

from sqlalchemy.orm import Session


def execute():
    with Session(get_engine()) as session:
        session.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm;');
        session.commit()