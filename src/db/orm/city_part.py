

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import typing
from ._defs import Base
from .city import City


class CityPart(Base):
    """"""
    # data
    city_part_id = Column(Integer, nullable=False, unique=True)
    name = Column(String, nullable=False, unique=False)
    city_id = Column(ForeignKey(City.city_id), unique=False)

    # meta
    __tablename__ = 'city_part'
    id = Column(Integer, primary_key=True)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())

    # relationships
    city = relationship(
        'City',
        foreign_keys='CityPart.city_id',
    )

    def __str__(self) -> str:
        return f'<City part {self.name}>'

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other) -> bool:
        return self.city_part_id == other.city_part_id

    def to_dict(self) -> typing.Dict:
        return {
            'region_id': self.district.region.region_id,
            'district_id': self.district.district_id,
            'city_id': self.city.city_id,
            'city_part_id': self.city_part_id,
            'name': self.name,
        }
