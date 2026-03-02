# from typing import Optional, Tuple, TypedDict
from location.utils.coordinates import LocationData

from django.utils.translation import gettext_lazy as _

from django.db.models import F

from rest_framework.response import Response
from rest_framework import status

from location.utils.utils import create_responce
from location.models import Building
from location.spatial_service import spatial_service

#  այս իմպորտները պետք են միայն հարցումները տպելու համար
from django.db import connection
from pprint import pprint

#


class CreateResponceByValidLocationData:
    def __init__(self, validated_data: LocationData, lang: str):
        self.lang = lang
        self.point = validated_data["point"]
        self.lat = validated_data["latitude"]
        self.lon = validated_data["longitude"]

    def get_rounded_coords(self, digits=4)->str:
        return f"{round(self.lat, digits)} {round(self.lon, digits)}"

    def create_responce(self):
        city_id, city_data = spatial_service.find_city(point=self.point)
        if not city_id:
            return Response(
                create_responce(
                    self.get_rounded_coords(),
                    _("Shirak region"),
                    db_obj_list=None,
                    latitude=self.lat,
                    longitude=self.lon,
                ),
                status=status.HTTP_200_OK,
            )
        geometry__contains = f"POINT({self.lat} {self.lon})"
        sity = city_data.get(f"city_{self.lang}")
        district = None
        if city_id == 1:
            district = spatial_service.find_district(point=self.point)

        qs = Building.objects.select_related("stret").filter(sity_id=city_id)
        if district:
            qs = qs.filter(district=district)

        qs = qs.filter(geometry__contains=geometry__contains).values(
            building=F("id"), adr=F("adres"), street=F(f"stret__name_{self.lang}")
        )

        db_data = next(iter(qs), None)
        pprint(connection.queries)  # սա պետք է հեռացնել վերջում
        return Response(
            create_responce(
                round_cords=self.get_rounded_coords(),
                sity=sity,
                db_obj_list=db_data,
                latitude=self.lat,
                longitude=self.lon,
            ),
            status=status.HTTP_200_OK,
        )

