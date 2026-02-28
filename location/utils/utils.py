from django.utils.translation import gettext_lazy as _

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
