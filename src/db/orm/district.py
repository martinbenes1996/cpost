

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import typing
from ._defs import Base
from .region import Region


class District(Base):
    """"""
    # data
    district_id = Column(Integer, nullable=False, unique=True)
    name = Column(String, nullable=False, unique=False)
    region_id = Column(Integer, ForeignKey(Region.region_id), unique=False)

    # meta
    __tablename__ = 'district'
    id = Column(Integer, primary_key=True)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())

    # relationships
    region = relationship(
        'Region',
        foreign_keys='District.region_id',
    )

    def __str__(self) -> str:
        return f'<District {self.name}>'

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other) -> bool:
        return self.district_id == other.district_id

    def to_dict(self) -> typing.Dict:
        return {
            'region_id': self.region.region_id,
            'district_id': self.district_id,
            'name': self.name,
        }
