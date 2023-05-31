

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from ._defs import Base


class Region(Base):
    """"""
    # data
    region_id = Column(Integer, nullable=False, unique=True)
    name = Column(String, nullable=False, unique=False)

    # meta
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())

    def __str__(self) -> str:
        return f'<Region {self.name}>'

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other):
        return self.region_id == other.region_id

    def to_dict(self):
        return {
            'region_id': self.region_id,
            'name': self.name,
        }
