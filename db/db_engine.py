import os
import sqlalchemy
import sqlalchemy.orm as orm
from contextlib import contextmanager
from app_config import basedir, db_schema


class DBEngine:
    _engine = None
    _session = None

    @staticmethod
    def create_db_engine():
        """Creates a db engine"""
        db_path = os.path.join(basedir, f"{db_schema}.db")
        DBEngine._engine = sqlalchemy.create_engine(url=f"sqlite:///{db_path}")
        return DBEngine._engine

    @staticmethod
    def get_db_engine():
        if DBEngine._engine is None:
            DBEngine._engine = DBEngine.create_db_engine()
            print("SQL engine created successfully")
        return DBEngine._engine

    @staticmethod
    @contextmanager
    def get_db_session():
        engine = DBEngine.get_db_engine()
        if DBEngine._session is None:
            session_factory = orm.sessionmaker(bind=engine)
            DBEngine._session = orm.scoped_session(session_factory)
            print("Session factory created successfully")

        try:
            session = DBEngine._session()
            yield session
            session.commit()
        except Exception as e:
            print(str(e))
            session.rollback()
            raise
        finally:
            session.close()
