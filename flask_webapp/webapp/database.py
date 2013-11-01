from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = None
db_session = None
Base = None


def init_db(database_uri):
    global engine, db_session, Base
    engine = create_engine(database_uri, convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
    Base = declarative_base()
    Base.query = db_session.query_property()


def create_all_table():
    import webapp.models
    Base.metadata.create_all(bind=engine)


def create_all_test_table():
    import webapp.models
    import imp
    imp.reload(webapp.models)

    create_all_table()


def drop_all_table():
    Base.metadata.drop_all(bind=engine)
