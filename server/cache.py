# global imports
import cpost
import time
# local imports
import db


def fill_db():
    for region in cpost.regions():
        for district in cpost.districts(region['id']):
            _log.info(f"fill_db: district {district['name']}")
            for city in cpost.cities(district['id']):
                db.insert_city({
                    'city_id': city['id'],
                    'city_name': city['name'],
                    'district_id': district['id'],
                    'district_name': district['name'],
                    'region_id': region['id'],
                    'region_name': region['name']
                })
                print(city)
            time.sleep(.3)

# logger
import logging
_log = logging.getLogger(__name__)

__all__ = ["fill_db"]
