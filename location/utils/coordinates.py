import re
from typing import Optional, Tuple

# --- PRECOMPILED REGEX (module load time) ---

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

# --- HELPERS ---

def _dms_to_decimal(deg, minutes, seconds, direction):
    value = float(deg) + float(minutes)/60 + float(seconds)/3600
    if direction.upper() in ('S', 'W'):
        value *= -1
    return value


def _normalize(number_str: str) -> float:
    return float(number_str.replace(',', '.'))


def _is_valid(lat: float, lng: float) -> bool:
    return -90 <= lat <= 90 and -180 <= lng <= 180


# --- PUBLIC API ---

def parse_coordinates(text: str) -> Tuple[bool, Optional[Tuple[float, float]]]:

    # geo:
    for m in GEO_RE.finditer(text):
        lat, lng = _normalize(m.group(1)), _normalize(m.group(2))
        if _is_valid(lat, lng):
            return True, (lat, lng)

    # DMS
    dms_matches = list(DMS_RE.finditer(text))
    if len(dms_matches) >= 2:
        lat = _dms_to_decimal(*dms_matches[0].groups())
        lng = _dms_to_decimal(*dms_matches[1].groups())
        if _is_valid(lat, lng):
            return True, (lat, lng)

    # Decimal
    for m in PAIR_RE.finditer(text):
        lat, lng = _normalize(m.group(1)), _normalize(m.group(2))
        if _is_valid(lat, lng):
            return True, (lat, lng)

    return False, None