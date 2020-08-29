# global imports
import cpost
import time
# local imports
import db


def fill_cities():
    for region in cpost.regions():
        for district in cpost.districts(region['id']):
            _log.info(f"fill_cities: district {district['name']}")
            for city in cpost.cities(district['id']):
                db.insert_city({
                    'city_id': city['id'],
                    'city_name': city['name'],
                    'district_id': district['id'],
                    'district_name': district['name'],
                    'region_id': region['id'],
                    'region_name': region['name']})
            time.sleep(.3)
            
def fill_addresses(region_id = None, district_id = None, city_id = None):
    # subset cities
    x = db.read_cities()
    if region_id is not None:
        x = filter(lambda i: i['region_id'] == region_id, x)
    if district_id is not None:
        x = filter(lambda i: i['district_id'] == district_id, x)
    if city_id is not None:
        x = filter(lambda i: i['city_id'] == city_id, x)
    # fetch city parts
    for city in x:
        for city_part in cpost.city_parts(city['city_id']):
            # city part addresses
            addresses = cpost.addresses(city_part_id=city_part['id'])
            for i,a in enumerate(addresses):
                addresses[i]['house_id'],addresses[i]['house_name'] = a['id'],a['name']
                addresses[i]['street_id'],addresses[i]['street_name'] = None,None
                addresses[i]['city_part_id'],addresses[i]['city_part_name'] = city_part['id'],city_part['name']
                addresses[i]['city_id'] = city['city_id']
                addresses[i]['city_name'] = city['city_name'] # to remove
                del addresses[i]['id']
                del addresses[i]['name']
            # street addresses
            for street in cpost.streets(city_part['id']):
                _log.info(f"fill_addresses: street {street['name']}")
                for address in cpost.addresses(street_id=street['id']):
                    # match city part and street addresses
                    for i,a in enumerate(addresses):
                        # match!
                        if a['house_id'] == address['id']:
                            addresses[i]['house_name'] = address['name']
                            addresses[i]['street_id'],addresses[i]['street_name'] = street['id'],street['name']
                            break
                    # no match!
                    else:
                        addresses.append({
                            'house_id': address['id'],'house_name': address['name'],
                            'street_id': street['id'],'street_name': street['name'],
                            'city_part_id': city_part['id'],'city_part_name': city_part['name'],
                            'city_id': city['city_id'],
                            'city_name': city['city_name'] # to remove
                        })
                time.sleep(.3)
            
            # insert into database
            _log.info("inserting into database")
            for a in addresses:
                #print(a['city_name'], a['city_part_name'], a['street_name'], a['house_name'])
                db.insert_address(a)
# logger
import logging
_log = logging.getLogger(__name__)

__all__ = ["fill_cities","fill_addresses"]
