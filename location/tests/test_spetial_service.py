import os
import django
from django.utils.translation import gettext_lazy as _
import unittest

from shapely.geometry import Point as ShapelyPoint

from location.spatial_service import SpatialService, ServiceAvailableSpaceConst

# Կարգավորում ենք Django միջավայրը
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vaedo.settings")
django.setup()


class TestServiceAvailableSpaceConst(unittest.TestCase):
    def setUp(self):
        self.sas = ServiceAvailableSpaceConst()
        self.lat, self.lng = 43.8, 40.75

    def test_valid_check_cord(self):
        self.assertTrue(self.sas._check_cord(self.lat, self.lng))

    def test_dntvalid_check_cord(self):
        self.assertFalse(self.sas._check_cord(self.lng, self.lat))


class TestChecSpatialService(unittest.TestCase):
    def setUp(self):
        self.sps = SpatialService()
        self.sps.load()
        self.avelable_point = ShapelyPoint(43.8, 40.75)
        self.dntavelable_point = ShapelyPoint(40, 43.75)
        self.gyumri = ShapelyPoint(43.83791017340687, 40.7914018548377)
        self.gyumri_data = (
            1,
            {
                "id": 1,
                "city": "Gyumri",
                "city_en": "Gyumri",
                "city_ru": "Гюмри",
                "city_hy": "Գյումրի",
            },
        )

    def test_avelable_point(self):
        self.assertTrue(self.sps.check_avelable(self.avelable_point))

    def test_dntavelable_point(self):
        self.assertFalse(self.sps.check_avelable(self.dntavelable_point))

    def test_find_gyumri(self):
        self.assertEqual(self.gyumri_data, self.sps.find_city(self.gyumri))

    def test_find_district(self):
        self.assertEqual(1, self.sps.find_district(self.gyumri))


# python -m unittest location.tests.test_spetial_service

if __name__ == "__main__":
    unittest.main()
