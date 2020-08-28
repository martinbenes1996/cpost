
import cpost

def fill_db():
    for region in cpost.regions():
        for district in cpost.districts(region['id']):
            print(district)

__all__ = ["fill_db"]
