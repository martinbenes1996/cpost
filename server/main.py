
import db
import cache

import cpost

def init():
    regions = [{'region_id': r['id'],'region_name': r['name']}
               for r in cpost.regions()]
    districts = [{'district_id': d['id'],'district_name': d['name']}
                 for r in regions for d in cpost.districts(r['region_id'])]
    db.initialize(regions, districts)
    cache.fill_db()
    
def run():
    regions = db._read_regions()
    districts = db._read_districts()
    #x = db.read_cities()
    print(districts)

# set logger
if __name__ == "__main__":
    import logging
    logging.basicConfig(level = logging.INFO)

if __name__ == "__main__":
    import sys
    if '--init' in sys.argv:
        init()
    else:
        run()