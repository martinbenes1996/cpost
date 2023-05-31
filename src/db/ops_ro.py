
import os
import typing
from . import handle
from .orm.region import Region
from .orm.district import District
from .orm.address import Address

def get_region(region_id: int) -> Region:
    with handle.Session() as session:
        q = (session.query(Region)
            .filter(Region.region_id == region_id))
        res = [r for r in q]
        if len(res) == 0:
            raise LookupError(f'region id {region_id} not found')
        session.expunge_all()
        return res[0]

def get_districts(region_id: int) -> typing.List[District]:
    with handle.Session() as session:
        q = (session.query(District)
            .filter(District.region_id == region_id))
        res = [r for r in q]
        if len(res) == 0:
            raise LookupError(f'districts with region id {region_id} not found')
        session.expunge_all()
        return res[0]

def get_address(
    city_part_id: int = None,
    street_id: int = None,
    address_id: int = None,
) -> typing.List[Address]:
    with handle.Session() as session:
        q = session.query(Address)
        if city_part_id is not None:
            q = q.filter(Address.city_part_id == city_part_id)
        if street_id is not None:
            q = q.filter(Address.street_id == street_id)
        if address_id is not None:
            q = q.filter(Address.address_id == address_id)
        res = [r for r in q]
        if len(res) == 0:
            raise LookupError(f'addresses with address id {address_id} not found')
        session.expunge_all()
        return res
