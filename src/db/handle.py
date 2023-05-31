
import sqlalchemy
from .orm import Base

def db_path() -> str:
    return 'db/cpost.sqlite'

def _engine():
    # singleton memory db
    mem_db = None

    def get_engine(inmemory=False):
        """Create database engine."""
        nonlocal mem_db

        # memory instance
        if inmemory:
            if mem_db is None:
                # print("In-memory SQLITE database created.")
                mem_db = sqlalchemy.create_engine(f'sqlite:///:memory:')
            # print("In-memory SQLITE database returned.")
            return mem_db

        # file (disk) instance
        else:
            return sqlalchemy.create_engine(f'sqlite:///{db_path()}')
	#
    return get_engine

engine = _engine()


class Session:
    maker = None
    @classmethod
    def get_maker(cls, inmemory=False):
        if cls.maker is None:
            cls.maker = sqlalchemy.orm.sessionmaker()
            cls.maker.configure(bind=engine(inmemory=inmemory))
        return cls.maker

    def __init__(self, inmemory=False, *args, **kw):
        self.session = self.get_maker(inmemory=inmemory)(*args, **kw)

    def __enter__(self):
        return self.session

    def __exit__(self, e_type, e_val, e_tback):
        if e_type is None:
            self.session.commit()
        else:
            self.session.rollback()

def create_schema(e):
    """Initialize database."""
    Base.metadata.create_all(e)

def drop_table(table):
    """Initialize database."""
    global engine
    print(f'Deleting table {table}')
    Base.metadata.drop_all(bind=engine, tables=[table], checkfirst=True)
