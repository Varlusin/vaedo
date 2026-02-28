import json
from shapely.geometry import shape
from shapely.prepared import prep
from shapely.strtree import STRtree
from django.conf import settings
import os


class SpatialService:
    def __init__(self):

        self.service_available_space = None

        self.city_polygons = []
        self.city_data = []
        self.city_tree = None

        self.district_polygons = []
        self.district_ids = []

        self.district_tree = None

    def load(self):
        self._load_cities()
        self._load_districts()
        self._load_avelable_space()

    def _load_avelable_space(self):
        path = os.path.join(
            settings.BASE_DIR, "location/data/SERVICE_AVAILABLE_SPACE.geojson"
        )
        with open(path, "r", encoding="utf-8") as f:
            geojson = json.load(f)

        features = geojson["features"][0]
        geom = shape(features["geometry"])
        self.service_available_space = prep(geom)

    def _load_cities(self):
        path = os.path.join(settings.BASE_DIR, "location/data/SITY_LIST.geojson")

        with open(path, "r", encoding="utf-8") as f:
            geojson = json.load(f)

        for feature in geojson["features"]:
            geom = shape(feature["geometry"])
            self.city_polygons.append(geom)
            self.city_data.append(
                {
                    "id": feature["properties"]["id"],
                    "city_en": feature["properties"]["sity_en"],
                    "city_ru": feature["properties"]["sity_ru"],
                    "city_hy": feature["properties"]["sity_hy"],
                }
            )

        self.city_tree = STRtree(self.city_polygons)

    def _load_districts(self):
        path = os.path.join(settings.BASE_DIR, "location/data/COMUNITY_DATA.geojson")

        with open(path, "r", encoding="utf-8") as f:
            geojson = json.load(f)

        for feature in geojson["features"]:
            geom = shape(feature["geometry"])
            self.district_polygons.append(geom)
            self.district_ids.append(feature["properties"]["id"])

        self.district_tree = STRtree(self.district_polygons)

    def check_avelable(self, point):
        if self.service_available_space.contains(point):
            return True
        return False

    def find_city(self, point):
        candidate_indexes = self.city_tree.query(point)

        for idx in candidate_indexes:
            polygon = self.city_polygons[idx]

            if polygon.contains(point):
                return self.city_data[idx]["id"], self.city_data[idx]

        return None, None

    def find_district(self, point):
        candidate_indexes = self.district_tree.query(point)

        for idx in candidate_indexes:
            polygon = self.district_polygons[idx]

            if polygon.contains(point):
                return self.district_ids[idx]

        return None


spatial_service = SpatialService()
