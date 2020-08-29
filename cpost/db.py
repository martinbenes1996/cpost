# global

# local
from . import _b2c as b2c
from . import _db

def regions():
    data = _db._read_regions()
    return data

def districts(region_id = None):
    def _districts(region_id):
        x = _db._read_districts()
        return filter(lambda i: i['region_id'] == region_id, data)
    # a certain region
    if region_id is not None: x = _districts(region_id)
    # all regions
    else: x = [_districts(r) for r in regions()]
    return [d for d in x]

def cities(district_id = None):
    def _cities(district_id):
        x = _db.read_cities()
        x = filter(lambda i: i['district_id'] == district_id, data)
        return x
    # a certain district
    if district_id is not None: x = _cities(district_id)
    # all districts
    else: x = [_cities(d) for d in districts()]
    return [c for c in x]

def city_parts(city_id):
    raise NotImplementedError
def streets(city_part_id):
    raise NotImplementedError
def addresses(street_id=None, city_part_id=None):
    raise NotImplementedError

__all__ = ["regions","districts","cities","city_parts","streets","addresses"]
