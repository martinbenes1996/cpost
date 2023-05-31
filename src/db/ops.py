
from . import handle
from .ops_ro import *
from .ops_rw import *

def remove_db():
    try:
        os.remove(handle.db_path())
    except FileNotFoundError:
        pass

def create_db():
    engine = handle.engine()
    handle.create_schema(engine)
