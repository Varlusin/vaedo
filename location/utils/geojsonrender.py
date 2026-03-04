from django.utils.translation import gettext_lazy as _

from typing import Optional, TypedDict, List, Dict


class Geometry(TypedDict):
    type: str  # "Point"
    coordinates: List[float] # [longitude, latitude]

class Properties(TypedDict):
    building:   str|None
    adres: str

class Feature(TypedDict):
    type: str # "Feature"
    properties: Properties
    geometry: Geometry

class GeojsonResponse(TypedDict):
    type: str # "FeatureCollection"
    features: List[Feature]



def GEOJSONRender(
    round_cords: str,
    sity: str,
    latitude: float,
    longitude: float,
    db_obj_list: Dict|None = None,
) -> Optional[GeojsonResponse]:
    try:
        if db_obj_list:
            building = db_obj_list["building"]
            if db_obj_list["street"]:
                sity = sity + " " + db_obj_list["street"]
                if db_obj_list["adr"]:
                    sity = sity + " " + db_obj_list["adr"]
                else:
                    sity = sity + " " + round_cords
            else:
                sity = sity + " " + round_cords
        else:
            sity = sity + " " + round_cords
            building = None

        return {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "building": building,
                        "adres": sity,
                    },
                    "geometry": {"type": "Point", "coordinates": [longitude, latitude]},
                },
            ],
        }
    except (ValueError, TypeError):
        return None
