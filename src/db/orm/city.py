

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import typing
from ._defs import Base
from .district import District


class City(Base):
    """"""
    # data
    city_id = Column(Integer, nullable=False, unique=True)
    name = Column(String, nullable=False, unique=False)
    district_id = Column(ForeignKey(District.id), unique=False)

    # meta
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())

    # relationships
    district = relationship(
        'District',
        foreign_keys='City.district_id',
    )

    def __str__(self) -> str:
        return f'<City {self.name}>'

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other) -> bool:
        return self.city_id == other.city_id

    def to_dict(self) -> typing.Dict:
        return {
            'region_id': self.district.region.region_id,
            'district_id': self.district.district_id,
            'city_id': self.city_id,
            'name': self.name,
        }
