
import sys
sys.path.append("..")

import cpost

def fill_db():
    for region in cpost.regions():
        print(region)

__all__ = ["fill_db"]
