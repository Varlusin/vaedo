import os
import django
import unittest

from django.utils.translation import gettext_lazy as _

from location.utils.geojsonrender import GEOJSONRender

# Կարգավորում ենք Django միջավայրը
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "vaedo.settings"
)  # Փոխարինեք "vaedo" ձեր նախագծի անունով
django.setup()


class TestGEOJSONRender(unittest.TestCase):
    def setUp(self):
        self.dont_find_cord = {
            "round_cords": "43.7907 40.8334",
            "sity": _("Shirak region"),
            "latitude": 43.79070038515901,
            "longitude": 40.833401337895886,
            "db_obj_list": None,
        }

        self.pnt_in_db = {
            "round_cords": "43.7907 40.8334",
            "sity": "Gyumri",
            "latitude": 43.845810484766766,
            "longitude": 40.808275984016554,
            "db_obj_list": {"building":2396,
                            "street":"Vazgen Sargsyan street",
                            "adr":"8а"
                            },
        }

        self.dont_find_cord_GJ = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "building": None,
                        "adres": "Shirak region 43.7907 40.8334",
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [40.833401337895886, 43.79070038515901],
                    },
                }
            ],
        }

        self.pnt_in_db_GJ = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "building": 2396,
                        "adres": "Gyumri Vazgen Sargsyan street 8а",
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [40.808275984016554, 43.845810484766766],
                    },
                }
            ],
        }

    def test_NoneGEOJSONRender(self):
        self.assertEqual(self.dont_find_cord_GJ, GEOJSONRender(**self.dont_find_cord))

    def test_GEOJSONRender(self):
        self.assertEqual(self.pnt_in_db, GEOJSONRender(**self.pnt_in_db))

# python -m unittest location.tests.test_geojsonrender


if __name__ == "__main__":
    unittest.main()
