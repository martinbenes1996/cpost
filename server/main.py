
import db
import cache

import cpost


def init():
    # fetch regions and districts
    regions = [{'region_id': r['id'],'region_name': r['name']}
               for r in cpost.regions()]
    districts = [{'district_id': d['id'],'district_name': d['name']}
                 for r in regions for d in cpost.districts(r['region_id'])]
    # initialize the database
    db.initialize(regions, districts)
    # fetch cities
    cache.fill_cities()

def f1():
    for city in db.read_cities():
        print(city)
    #cache.fill_addresses(city_id=4880)
    # Tetčice 5185
    # Rybniky 4424
    # Střelice 4880
    # Brno 361
    
def f2():
    #regions = db._read_regions()
    #districts = db._read_districts()
    x = db.read_addresses()
    print([i for i in x])
    #x = db.read_cities()
    #x = filter(lambda i: i['city_name'] == "Brno", x)
    #print([i for i in x])

# set logger
if __name__ == "__main__":
    import logging
    logging.basicConfig(level = logging.INFO)

if __name__ == "__main__":
    import sys
    if '-f2' in sys.argv:
        f2()
    elif '--init' in sys.argv:
        print('All database is about to be rewritten.')
        input('Press any key to continue...')
        init()
        
    else:
        f1()