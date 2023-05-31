""""""
import warnings
import pkg_resources
import requests
import typing

from . import _b2c as b2c

def regions(
) -> typing.List:
    """Fetch regions."""
    rs = b2c.json('/services/Address/getRegionListAsJson')
    rs = [
        {
            'region_id': int(r['id']),
            'name': r['name']
        }
        for r in rs
    ]
    rs = sorted(rs, key=lambda k: k['region_id'])
    return rs

def districts(
    region_id: typing.Union[str, int],
) -> typing.List:
    """Fetch districts of given region."""
    # parse input
    region_id = int(region_id)
    # fetch
    ds = b2c.json(
        '/services/Address/getDistrictListAsJson',
        params={"id": region_id}
    )
    # parse output
    ds = map(
        lambda d: {
            'region_id': region_id,
            'district_id': int(d['id']),
            'name': d['name']
        },
        ds
    )
    ds = sorted(ds, key=lambda k: k['district_id'])
    return list(ds)

def cities(
    district_id: typing.Union[str, int],
) -> typing.List:
    """Fetch cities from given district."""
    # parse input
    district_id = int(district_id)
    # fetch
    cs = b2c.json(
        '/services/Address/getCityListAsJson',
        params={"id": district_id}
    )
    # parse output
    cs = map(
        lambda c: {
            'district_id': district_id,
            'city_id': int(c['id']),
            'name': c['name']
        },
        cs
    )
    cs = sorted(cs, key=lambda k: k['city_id'])
    return list(cs)

def city_parts(
    city_id: typing.Union[str, int],
) -> typing.List:
    """Get city parts from given city."""
    # parse input
    city_id = int(city_id)
    # fetch
    cps = b2c.json(
        '/services/Address/getCityPartListAsJson',
        params={"id": city_id}
    )
    # parse output
    cps = map(
        lambda cp: {
            'city_id': city_id,
            'city_part_id': int(cp['id']),
            'name': cp['name']
        },
        cps
    )
    cps = sorted(cps, key=lambda k: k['city_part_id'])
    return list(cps)

def streets(
    city_part_id: typing.Union[str, int],
) -> typing.List:
    """Get city parts from given city."""
    # parse input
    city_part_id = int(city_part_id)
    # fetch
    ss = b2c.json(
        '/services/Address/getStreetListAsJson',
        params={"id": city_part_id},
    )
    # parse output
    ss = map(
        lambda s: {
            'city_part_id': city_part_id,
            'street_id': int(s['id']),
            'name': s['name']
        },
        ss
    )
    ss = sorted(ss, key=lambda k: k['street_id'])
    return list(ss)

def addresses(
    street_id: typing.Union[str, int] = None,
    city_part_id: typing.Union[str, int] = None,
) -> typing.List:
    # parse input
    assert bool(street_id) ^ bool(city_part_id), 'one of street_id or city_part_id must be given'
    if street_id:
        params = {'idStreet': int(street_id)}
    if city_part_id:
        params = {'idCityPart': int(city_part_id)}
    # fetch
    ns = b2c.json('/services/Address/getNumberListAsJson', params=params)
    # parse output
    ns = map(
        lambda n: {
            'city_part_id': city_part_id,
            'street_id': street_id,
            'address_id': int(n['id']),
            'name': n['name']
        },
        ns
    )
    ns = sorted(ns, key=lambda k: k['address_id'])
    return list(ns)

__all__ = ['regions', 'districts', 'cities', 'city_parts', 'streets', 'addresses']
