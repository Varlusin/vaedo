from django.utils.translation import gettext_lazy as _

from shapely.geometry import Point as ShapelyPoint

from django.core.cache import cache


SERVICE_AVAILABLE_SPACE = cache.get("SERVICE_AVAILABLE_SPACE")
SITY_LIST = cache.get("SITY_LIST")
COMUNITY_DATA = cache.get("COMUNITY_DATA")


class CheckRequestLocation:
    """Ստուգում է latitude և longitude կոորդինատների վավերականությունը և վերադարձնում է համապատասխան տվյալներ"""

    def __init__(
        self,
        lang: str,
        latitude: str = None,
        longitude: str = None,
    ) -> None:
        self.lang = lang if lang else "en"
        self.latitude: float = self._to_float(latitude)
        self.longitude: float = self._to_float(longitude)
        self.is_valid, self.reason_validation = self._validate_coordinates()
        self.point = (
            ShapelyPoint(self.latitude, self.longitude) if self.is_valid else None
        )
        self.round_cords = self._round_coordinates() if self.is_valid else None

    def _to_float(self, value: str) -> float:
        """Փոխակերպում է արժեքը float-ի, եթե հնարավոր է"""
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    def _round_coordinates(self, round_num: int = 4) -> str:
        """Կլորացնում է latitude և longitude արժեքները"""
        return f"{round(self.longitude, round_num)} {round(self.latitude, round_num)}"

    def _validate_coordinates(self) -> tuple[bool, str]:
        """Ստուգում է կոորդինատների վավերականությունը"""
        if self.latitude is None or self.longitude is None:
            return False, _("Invalid request")

        if not (43.76 <= self.latitude <= 43.9264) or not (
            40.706 <= self.longitude <= 40.855
        ):
            return False, {
                "detail": _(
                    "Sorry, the service is not available at the specified location."
                )
            }

        if not ShapelyPoint(self.latitude, self.longitude).within(
            SERVICE_AVAILABLE_SPACE
        ):
            return False, {
                "detail": _(
                    "Sorry, the service is not available at the specified location."
                )
            }

        return True, None

    def create_request_data(self) -> tuple[bool, dict, dict]:
        """Ստեղծում է հարցման տվյալներ, եթե կոորդինատները վավեր են"""
        if not self.is_valid:
            raise ValueError(
                "The coordinates are not valid. Please check the coordinates."
            )

        data = next(
            (
                {
                    "sity": sity[f"sity_{self.lang}"],
                    "id": sity["id"],
                }
                for sity in SITY_LIST
                if self.point.within(sity["geometry"])
            ),
            None,
        )

        if not data:
            return None, _("Shirak region")

        if data["id"] == 1:
            data["community_id"] = next(
                (
                    community["id"]
                    for community in COMUNITY_DATA
                    if self.point.within(community["geometry"])
                ),
                None,
            )

        return (
            True,
            {
                "sity_id": data["id"],
                "geometry__contains": f"POINT({self.latitude} {self.longitude})",
                "district": data.get("community_id"),
                "sity": data["sity"],
            },
        )


def create_responce(
    round_cords: str,
    sity: str,
    db_obj_list: list = None,
    latitude: float = None,
    longitude: float = None,
) -> dict[
    str,
    list[
        dict[
            str,
            dict,
            dict,
        ]
    ],
]:
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
            building =None

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
