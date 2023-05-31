""""""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import typing
from ._defs import Base
from .city_part import CityPart
from .street import Street


class Address(Base):
    """"""
    # data
    address_id = Column(Integer, nullable=False, unique=True)
    name = Column(String, nullable=False, unique=False)
    city_part_id = Column(ForeignKey(CityPart.id), unique=False, nullable=True)
    street_id = Column(ForeignKey(Street.id), unique=False, nullable=True)

    # meta
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())

    # relationships
    city_part = relationship(
        'CityPart',
        foreign_keys='Address.city_part_id',
    )
    street = relationship(
        'Street',
        foreign_keys='Address.street_id',
    )

    def __str__(self) -> str:
        return f'<Address {self.name}>'

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other) -> bool:
        return self.address_id == other.address_id

    def to_dict(self) -> typing.Dict:
        return {
            'region_id': self.district.region.region_id,
            'district_id': self.district.district_id,
            'city_id': self.city.city_id,
            'city_part_id': self.city_part.city_part_id if self.city_part else None,
            'street_id': self.street.street_id if self.street else None,
            'address_id': self.address_id,
            'name': self.name,
        }
