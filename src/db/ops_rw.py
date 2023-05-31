
from . import handle
from .orm.region import Region
from .orm.district import District
from .orm.city import City
from .orm.address import Address

def insert_region(
    region_id: int,
    name: str,
):
    """"""
    with handle.Session() as session:
        # create item
        region = Region(
            region_id=region_id,
            name=name,
        )
        # add item
        session.add(region)
        session.commit()

def insert_district(
    district_id: int,
    name: str,
    region_id: int,
):
    """"""
    with handle.Session() as session:
        # create item
        district = District(
            district_id=district_id,
            name=name,
            region_id=region_id,
        )
        # add item
        session.add(district)
        session.commit()

def insert_city(
    city_id: int,
    name: str,
    region_id: int,
    district_id: int,
):
    """"""
    with handle.Session() as session:
        # create item
        district = City(
            district_id=district_id,
            name=name,
            region_id=region_id,
        )
        # add item
        session.add(district)
        session.commit()

def update_address(
    address_id: int,
    **update_dict,
):
    """"""
    with handle.Session() as session:
        # update item
        q = (session.query(Address)
            .filter(Address.address_id == address_id)
            .update(update_dict))
        session.commit()
