
import functools
import pkg_resources
import sqlite3

def dbaccess(dbname):
    def dbaccess_wrapper(fn):
        @functools.wraps(fn)
        def fn_replace(*args, **kw):
            # connect
            fname = pkg_resources.resource_filename(__name__, dbname)
            conn = sqlite3.connect(fname)
            
            x = fn(conn.cursor(), *args, **kw) # run command
            
            conn.commit() # commit
            conn.close()
            return x
        return fn_replace
    return dbaccess_wrapper

@dbaccess("../sql/data.db")
def initialize(c, regions, districts):
    query_regions = '''
    CREATE TABLE IF NOT EXISTS regions (
        region_id INTEGER PRIMARY KEY,
        region_name TEXT NOT NULL
    )'''
    c.execute(query_regions)
    query_districts = '''
    CREATE TABLE IF NOT EXISTS districts (
        district_id INTEGER PRIMARY KEY,
        district_name TEXT NOT NULL
    )'''
    c.execute(query_districts)
    query_cities = '''
    CREATE TABLE IF NOT EXISTS cities (
        city_id INTEGER PRIMARY KEY,
        city_name TEXT NOT NULL,
        district_id INTEGER NOT NULL,
        region_id INTEGER NOT NULL
    )'''
    c.execute(query_cities)
    query_addresses = '''
    CREATE TABLE IF NOT EXISTS addresses (
        house_id INTEGER PRIMARY KEY,
        house_name TEXT NOT NULL,
        street_id INTEGER,
        street_name TEXT,
        city_part_id INTEGER,
        city_part_name TEXT,
        city_id INTEGER NOT NULL
    )'''
    c.execute(query_addresses)
    # empty tables
    c.execute('DELETE FROM regions')
    c.execute('DELETE FROM districts')
    c.execute('DELETE FROM cities')
    c.execute('DELETE FROM addresses')
    # insert regions and districts
    c.executemany('INSERT INTO regions VALUES (?,?)',
                  [(r['region_id'],r['region_name']) for r in regions])
    c.executemany('INSERT INTO districts VALUES (?,?)',
                  [(d['district_id'],d['district_name']) for d in districts])
    _log.info("database initialized")

bypass = lambda x: x
def tryInt(i):
    try: return int(i)
    except: i
city_cols = ['city_id','city_name','district_id','region_id']
city_f = [int, bypass, int, bypass, int, bypass]
address_cols = ['house_id','house_name','street_id','street_name','city_part_id','city_part_name','city_id']
address_f = [int, bypass, tryInt, bypass, int, bypass, int]

@dbaccess("../sql/data.db")
def insert_city(c, data):
    record = tuple([f(data[k]) for f,k in zip(city_f,city_cols)])
    c.execute('INSERT INTO cities VALUES (?,?,?,?)',record)
@dbaccess("../sql/data.db")
def insert_address(c, data):
    record = tuple([f(data[k]) for f,k in zip(address_f,address_cols)])
    c.execute('INSERT INTO addresses VALUES (?,?,?,?,?,?,?)',record)
@dbaccess("../sql/data.db")
def _read_regions(c):
    c.execute('SELECT * FROM regions')
    x = c.fetchall()
    return {r[0]: r[1] for r in x}
@dbaccess("../sql/data.db")
def _read_districts(c):
    c.execute('SELECT * FROM districts')
    x = c.fetchall()
    return {d[0]: d[1] for d in x}
@dbaccess("../sql/data.db")
def read_cities(c):
    c.execute('SELECT * FROM cities')
    x = c.fetchall()
    regions,districts = _read_regions(),_read_districts()
    x = [{col: xij for col,xij in zip(city_cols,xi)} for xi in x]
    return [{**city,
             'region_name': regions[city['region_id']],
             'district_name': districts[city['district_id']]} for city in x]
@dbaccess("../sql/data.db")
def read_addresses(c):
    c.execute('SELECT * FROM addresses')
    x = c.fetchall()
    return [{col: xij for col,xij in zip(address_cols,xi)} for xi in x]

# logger
import logging
_log = logging.getLogger(__name__)

__all__ = ["initialize",
           "insert_city","insert_address",
           "read_cities","read_addresses",
           "_read_regions","_read_districts"]