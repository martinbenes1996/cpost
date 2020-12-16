
from datetime import datetime
import unittest

import cpost

class TestApi(unittest.TestCase):
    def test_regions(self):
        x = cpost.api.regions()
        self.assertIsInstance(x, dict)
        self.assertTrue(len(x) == 14)
        for r in range(1,14):
            self.assertIn(r, region.keys())
        for r in ['Hlavní město Praha','Jihočeský','Jihomoravský','Karlovarský',
                  'Královéhradecký','Liberecký','Moravskoslezský','Olomoucký',
                  'Pardubický','Plzeňský','Středočeský','Ústecký','Vysočina','Zlínský']:
            self.assertIn(r, x.values())
        print("Tested")
    def test_districts(self):
        x = cpost.api.districts(11)
    def test_cities(self):
        x = cpost.api.cities(55)
    def test_city_parts(self):
        x = cpost.api.city_parts(5185)
    def test_streets(self):
        x = cpost.api.streets(12501)
    def test_addresses(self):
        x = cpost.api.addresses(28783)

__all__ = ["TestApi"]
        