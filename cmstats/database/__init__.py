from cmstats.database.base import AbstractTable
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker


DBSession = scoped_session(sessionmaker())
Base = declarative_base(cls=AbstractTable)

def init_database(engine):
    DBSession.configure(bind=engine)

    # Import ORM mapped objects.
    __import__("cmstats.database.schema", globals(), locals(), ["*"])

    # Bind metadata to engine.
    Base.metadata.bind = engine

    # Create all tables (if necessary)
    Base.metadata.create_all(engine)
