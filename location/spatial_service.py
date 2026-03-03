import json
from shapely.geometry import shape
from shapely.geometry import Point as ShapelyPoint
from shapely.prepared import prep
from shapely.strtree import STRtree
from django.conf import settings
import os

from typing import Optional, Tuple, TypedDict

class CitiData(TypedDict):
    """
    Բառարան Քաղաքի կամ Գյուղի եռալեզու անվանումների և DB ID ով։
    """
    id: int
    city: str
    city_en: str
    city_ru: str
    city_hy: str




class ServiceAvailableSpaceConst:
    """
    Ծառայության Հասանելի տարածքի մեծագույն և փոքրագույն կորդինատներով կլասս 

        ```python
            self.min_lat= 43.76
            self.max_lat= 43.9264
            self.min_lng= 40.706
            self.max_lng = 40.855
        ``` 
    """
    def __init__(self):
        self.min_lat= 43.76
        self.max_lat= 43.9264
        self.min_lng= 40.706
        self.max_lng = 40.855
    
    def _check_cord(self, lat:float, lng:float)->bool:
        """
        Վերադարձնում է այո կամ ոչ
        ### Օրինակ

        ```python
            >>> SASC =  ServiceAvailableSpaceConst()
            >>> SASA._check_cord(lat = 43.8, lng=40.75)
            True
        ```
        """
        return self.min_lat<= lat <= self.max_lat and self.min_lng<= lng<= self.max_lng



class SpatialService:
    """ Կլասս որը պահպանում է ծառայության հասանելի տարածքը, քաղաքների և թաղամասերի պոլիգոնները և տրամադրում է մեթոդներ կորդինատների վերլուծության համար։ """
    def __init__(self):

        self.service_available_space = None

        self.city_polygons = []
        self.city_data = []
        self.city_tree = None

        self.district_polygons = []
        self.district_ids = []
        self.district_tree = None

    def load(self):
        """ Բեռնում է ծառայության հասանելի տարածքը, քաղաքների և թաղամասերի պոլիգոնները։ """
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
                    "city": feature["properties"]["sity"],
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

    def check_avelable(self, point:ShapelyPoint)->bool:
        """ Ստուգում է արդյոք կորդինատները գտնվում են ծառայության հասանելի տարածքում։ 
            ### ՕՐԻՆԱԿ

            ```python
                >>> spatial_service = SpatialService()
                >>> spatial_service.load()
                >>> point = ShapelyPoint(40.75, 43.8)
                >>> spatial_service.check_avelable(point)
                True
            ```
        """
        if self.service_available_space.contains(point): # type: ignore
            return True
        return False

    def find_district(self, point:ShapelyPoint)-> Optional[int]:
        """
        Ստուգում է արդյոք կորդինատները Գյումրու որ թաղամասում է վերադարձնում է թաղամասի DB_ID հակառակ դեպքում None։ 
        """
        candidate_indexes = self.district_tree.query(point) # type: ignore

        for idx in candidate_indexes:
            polygon = self.district_polygons[idx]

            if polygon.contains(point):
                return self.district_ids[idx]

        return None
    

    def find_city(self, point:ShapelyPoint)-> Tuple[int|None ,CitiData|None]:
        """ Ստուգում է արդյոք կորդինատները գտնվում են ծառայության հասանելի Քաղաք կամ Գյուղերում եթե այո վերադարձնում է db_id և եռալեզու անվանում։ 
            ### ՕՐԻՆԱԿ

            ```python
                >>> spatial_service = SpatialService()
                >>> spatial_service.load()
                >>> point = ShapelyPoint(40.7914018548377, 43.83791017340687)
                >>> spatial_service.find_city(point)
                (1, {'id': 1,'sity': 'Gyumri', 'sity_en': 'Gyumri', 'sity_ru': 'Гюмри', 'sity_hy': 'Գյումրի'})
            ```
        """
        candidate_indexes = self.city_tree.query(point) # type: ignore

        for idx in candidate_indexes:
            polygon = self.city_polygons[idx]

            if polygon is None:
                continue  # Skip None polygons

            if polygon.contains(point):
                return self.city_data[idx]["id"], self.city_data[idx]

        return None, None



spatial_service = SpatialService()

SASC =  ServiceAvailableSpaceConst()
