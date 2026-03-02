import re
from typing import Optional, Tuple, TypedDict

from location.spatial_service import SASC, spatial_service

from shapely.geometry import Point as ShapelyPoint

# Սահմանում ենք բառարանի կառուցվածքը
class LocationData(TypedDict):
    latitude: float
    longitude: float
    point: ShapelyPoint




DECIMAL_RE = r'-?\d+(?:[.,]\d+)?'

GEO_RE = re.compile(
    rf'geo:\s*({DECIMAL_RE})\s*,\s*({DECIMAL_RE})',
    re.IGNORECASE
)

PAIR_RE = re.compile(
    rf'(?<!/)\b({DECIMAL_RE})\b(?!/)[,\s]+(?<!/)\b({DECIMAL_RE})\b(?!/)'
)

DMS_RE = re.compile(
    r'(\d+)[°\s]+(\d+)[\'\s]+(\d+(?:\.\d+)?)[\"\s]*([NSEW])',
    re.IGNORECASE
)

def _dms_to_decimal(deg, minutes, seconds, direction):
    value = float(deg) + float(minutes)/60 + float(seconds)/3600
    if direction.upper() in ('S', 'W'):
        value *= -1
    return value


def _normalize(number_str: str) -> float:
    return float(number_str.replace(',', '.'))


def _is_valid(lat: float, lng: float) -> Tuple[bool, Optional[LocationData]]:
    if not SASC._check_cord(lat=lat, lng=lng):
        if SASC._check_cord(lat=lng, lng=lat):
            lat, lng = lng, lat
        else: return False, None
    point = ShapelyPoint(lat, lng)
    if  spatial_service.check_avelable(point=point):
        validated_data = {"latitude": lat, "longitude": lng, "point":point}
        return True,  validated_data 
    return False, None



def parse_coordinates(text: str) -> Tuple[bool, Optional[LocationData]]:

    # geo:
    for m in GEO_RE.finditer(text):
        lat, lng = _normalize(m.group(1)), _normalize(m.group(2))
        is_valid, data  = _is_valid(lat=lat, lng=lng)
        if is_valid:
            return True, data

    # DMS
    dms_matches = list(DMS_RE.finditer(text))
    if len(dms_matches) >= 2:
        lat = _dms_to_decimal(*dms_matches[0].groups())
        lng = _dms_to_decimal(*dms_matches[1].groups())
        is_valid, data  = _is_valid(lat=lat, lng=lng)
        if is_valid:
            return True, data

    # Decimal
    for m in PAIR_RE.finditer(text):
        lat, lng = _normalize(m.group(1)), _normalize(m.group(2))
        is_valid, data  = _is_valid(lat=lat, lng=lng)
        if is_valid:
            return True, data

    return False, None