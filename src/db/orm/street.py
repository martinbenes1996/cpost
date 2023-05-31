""""""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import typing
from ._defs import Base
from .city_part import CityPart


class Street(Base):
    """"""
    # data
    street_id = Column(Integer, nullable=False, unique=False)
    name = Column(String, nullable=False, unique=False)
    city_part_id = Column(ForeignKey(CityPart.city_part_id), unique=False)
    __table_args__ = (
        UniqueConstraint('street_id', 'city_part_id', name='_city_part_street_uc'),
    )

    # meta
    __tablename__ = 'street'
    id = Column(Integer, primary_key=True)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())


    # relationships
    city_part = relationship(
        'CityPart',
        foreign_keys='Street.city_part_id',
    )

    def __str__(self) -> str:
        return f'<Street {self.name}>'

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other) -> bool:
        return self.street_id == other.street_id

    def to_dict(self) -> typing.Dict:
        return {
            'region_id': self.district.region.region_id,
            'district_id': self.district.district_id,
            'city_id': self.city.city_id,
            'city_part_id': self.city_part_id,
            'street_id': self.street_id,
            'name': self.name,
        }
