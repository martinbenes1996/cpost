
import cpost
import db
from tqdm import tqdm

def main():

    # # reset database
    # db.ops.remove_db()
    db.ops.create_db()

    # # fetch regions from api
    # regions = cpost.api.regions()
    # # save regions in the database
    # with db.handle.Session() as session:
    #     for r in tqdm(regions):
    #         region = db.Region(
    #             region_id=r['region_id'],
    #             name=r['name'],
    #         )
    #         session.add(region)
    #         session.commit()

    # # load regions from db
    # with db.handle.Session() as session:
    #     q = session.query(db.Region)
    #     regions = [r for r in q]
    #     session.expunge_all()
    # # per each region
    # for r in tqdm(regions):
    #     # fetch districts from api
    #     districts = cpost.api.districts(r.region_id)
    #     # store districts in db
    #     for d in districts:
    #         district = db.District(
    #             district_id=d['district_id'],
    #             name=d['name'],
    #             region_id=r.region_id,
    #         )
    #         session.add(district)
    #         session.commit()

    # # load districts from db
    # with db.handle.Session() as session:
    #     q = session.query(db.District)
    #     districts = [d for d in q]
    #     session.expunge_all()
    # # per each district
    # for d in tqdm(districts):
    #     # fetch cities from api
    #     cities = cpost.api.cities(d.district_id)
    #     # store cities in db
    #     for c in cities:
    #         city = db.City(
    #             city_id=c['city_id'],
    #             name=c['name'],
    #             district_id=d.district_id,
    #         )
    #         session.add(city)
    #         session.commit()

    # # load cities from db
    # with db.handle.Session() as session:
    #     q = session.query(db.City)
    #     cities = [c for c in q]
    #     session.expunge_all()
    # # per each city
    # for c in tqdm(cities):
    #     # fetch city parts from api
    #     city_parts = cpost.api.city_parts(c.city_id)
    #     # store city parts in db
    #     for cp in city_parts:
    #         city_part = db.CityPart(
    #             city_part_id=cp['city_part_id'],
    #             name=cp['name'],
    #             city_id=c.city_id,
    #         )
    #         session.add(city_part)
    #         session.commit()

    # # load city parts from db
    # with db.handle.Session() as session:
    #     q = session.query(db.CityPart)
    #     city_parts = [cp for cp in q]
    #     session.expunge_all()
    # # per each city part
    # for cp in tqdm(city_parts):
    #     # fetch streets from api
    #     streets = cpost.api.streets(cp.city_part_id)
    #     # store streets in db
    #     for s in streets:
    #         with db.handle.Session() as session:
    #             street = db.Street(
    #                 street_id=s['street_id'],
    #                 name=s['name'],
    #                 city_part_id=cp.city_part_id,
    #             )
    #             session.add(street)
    #             session.commit()

    # # load streets from db
    # with db.handle.Session() as session:
    #     q = session.query(db.Street)
    #     streets = [s for s in q]
    #     session.expunge_all()
    # # per each street
    # with db.handle.Session() as session:
    #     for s in tqdm(streets):
    #         # skip if exists
    #         q = (session.query(db.Address)
    #             .filter(db.Address.street_id == s.street_id))
    #         if q.first() is not None: continue
    #         # fetch addresses from api
    #         try:
    #             addresses = cpost.api.addresses(street_id=s.street_id)
    #         except TypeError:
    #             print(s.street_id)
    #             raise
    #         # store addresses in db
    #         for a in addresses:
    #             address = db.Address(
    #                 address_id=a['address_id'],
    #                 name=a['name'],
    #                 street_id=s.street_id,
    #             )
    #             session.add(address)
    #             session.commit()

    # load city parts from db
    with db.handle.Session() as session:
        q = session.query(db.CityPart)
        city_parts = [cp for cp in q]
    # per each city part
    for cp in tqdm(city_parts):
        # # skip if exists
        # q = (session.query(db.Address)
        #     .filter(db.Address.city_part_id == cp.city_part_id))
        # if q.first() is not None: continue
        # fetch addresses from api
        addresses = cpost.api.addresses(city_part_id=cp.city_part_id)
        # store addresses in db
        with db.handle.Session() as session:
            address_ids = [a['address_id'] for a in addresses]
            q = (session.query(db.Address)
                .filter(db.Address.address_id.in_(address_ids))
                .update({'city_part_id': cp.city_part_id}))
            # for a in addresses:
            #     # update existing address record
            #     try:
            #         existing_address = db.ops.get_address(
            #             address_id=a['address_id']
            #         )
            #         q = (session.query(db.Address)
            #             .filter(db.Address.address_id == a['address_id'])
            #             .update({'city_part_id': cp.city_part_id}))
            #         # db.ops.update_address(
            #         #     a['address_id'],
            #         #     city_part_id=cp.city_part_id,
            #         # )
            #     # create new address record
            #     except LookupError:
            #         address = db.Address(
            #             address_id=a['address_id'],
            #             name=a['name'],
            #             city_part_id=cp.city_part_id,
            #         )
            #         session.add(address)
            session.commit()

    return



    # fetch districts
    districts = [
        cpost.api.districts(r['region_id'])
        for r in regions
    ]
    districts = [d for rds in districts for d in rds]
    districts = districts[1:2]
    print('Districts:')
    print(districts)

    # fetch cities
    cities = [
        cpost.api.cities(d['district_id'])
        for d in districts
    ]
    cities = [
        {'region_id': d['region_id'], **c}
        for d, rcs in zip(districts, cities)
        for c in rcs
    ]
    cities = cities[:1]
    print('Cities:')
    print(cities)

    # fetch city parts
    city_parts = [
        cpost.api.city_parts(c['city_id'])
        for c in cities
    ]
    city_parts = [
        {
            'region_id': c['region_id'],
            'district_id': c['district_id'],
            **cp,
        }
        for c, rcps in zip(cities, city_parts)
        for cp in rcps
    ]
    city_parts = city_parts[1:2]
    print('City parts:')
    print(city_parts)

    # fetch streets
    streets = [
        cpost.api.streets(cp['city_part_id'])
        for cp in city_parts
    ]
    streets = [
        {
            'region_id': cp['region_id'],
            'district_id': cp['district_id'],
            'city_id': cp['city_id'],
            **s,
        }
        for cp, rss in zip(city_parts, streets)
        for s in rss
    ]
    streets = streets[15:16]
    print('Streets:')
    print(streets)

    # fetch addresses
    addresses = [
        cpost.api.addresses(s['street_id'])
        for s in streets
    ]
    addresses = [
        {
            'region_id': s['region_id'],
            'district_id': s['district_id'],
            'city_id': s['city_id'],
            'city_part_id': s['city_part_id'],
            **a,
        }
        for s, ras in zip(streets, addresses)
        for a in ras
    ]
    print('Addresses:')
    print(addresses)

    # # x = cpost.api.streets(12501)
    # x = cpost.api.addresses(city_part_id=12501)  # 28783)#, 12501)
    # print(x)

if __name__ == '__main__':
    main()