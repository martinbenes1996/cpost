
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
def initialize(c):
    cities = '''
    CREATE TABLE IF NOT EXISTS cities (
        city_id INTEGER PRIMARY KEY,
        city_name TEXT NOT NULL,
        district_id INTEGER NOT NULL,
        district_name TEXT NOT NULL,
        region_id INTEGER NOT NULL,
        region_name TEXT NOT NULL
    )'''
    c.execute(cities)
    addresses = '''
    CREATE TABLE IF NOT EXISTS addresses (
        house_id INTEGER PRIMARY KEY,
        house_name TEXT NOT NULL,
        street_id INTEGER,
        street_name TEXT,
        city_part_id INTEGER,
        city_part_name TEXT,
        city_id INTEGER NOT NULL
    )'''
    c.execute(addresses)  

@dbaccess("../sql/data.db")
def insert_city(c, data):
    record = (int(data['city_id']),
              data['city_name'],
              int(data['district_id']),
              data['district_name'],
              int(data['region_id']),
              data['region_name'])    
    c.execute('INSERT INTO cities VALUES (?,?,?,?,?,?)',record)
@dbaccess("../sql/data.db")
def insert_address(c, data):
    record = (int(data['house_id']),
              data['house_name'],
              int(data['street_id']),
              data['street_name'],
              int(data['city_part_id']),
              data['city_part_name'],
              int(data['city_id']))
    c.execute('INSERT INTO addresses VALUES (?,?,?,?,?,?,?)',record)