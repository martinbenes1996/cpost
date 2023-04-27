
import cpost

def main():
    # fetch regions
    regions = cpost.api.regions()
    regions = regions[10:11]
    print('Regions:')
    print(regions)

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