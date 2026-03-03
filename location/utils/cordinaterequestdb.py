from location.utils.coordinates import LocationData

from django.utils.translation import gettext_lazy as _

from django.db.models import F

from rest_framework.response import Response
from rest_framework import status

from location.utils.utils import create_responce as GeoJsonSerializer
from location.models import Building
from location.spatial_service import spatial_service

from typing import cast

#  այս իմպորտները պետք են միայն հարցումները տպելու համար
# from django.db import connection
# from pprint import pprint

#


class CreateResponceByValidLocationData:
    """
    Կլասը ստեղծում և վերադարձնում է HTTPResponce պատասխան՝ GeoJson   կատարելով DB կետի (միայն վավեր կորդինատներ) կորդինատներով։  
    """
    def __init__(self, validated_data: LocationData, lang: str)->None:
        self.lang = lang
        self.point = validated_data["point"]
        self.lat = validated_data["latitude"]
        self.lon = validated_data["longitude"]

    def _get_rounded_coords(self, digits:int = 4)->str:
        """
        Հետ է վերադարձնում կետի կորդինատների կլորացված (defoult 4 նիշով) տեքստը (str)։ 
        """
        return f"{round(self.lat, digits)} {round(self.lon, digits)}"

    def create_responce(self)->Response:
        """
        Մեթոդը սկզբում պարզում է կետը պատկանում է որևէ քաղաքի եթե չի պատքանում հետ է վերադարձնում պատասխան այն մասին որ կետը շիրակի մարզում է կետի կորդինատները և այն որ ծառայությունը այդ տարածքում հասանելի է։

        եթե կետը գյումրիում է պարզում է նաև որ թաղամասում է (Նախորոք փորձում է հեշտացնել սպասվելիք DB հարցումը)
        ստացված id ֊ներով հարցում է կատարում db արդյունքները դարցնում httpResponce և հետ վերադարցնում։
        """
        city_id, city_data = spatial_service.find_city(point=self.point)
        if not city_id:
            return Response(
                GeoJsonSerializer(
                    self._get_rounded_coords(),
                    sity= _("Shirak region"),
                    latitude=self.lat,
                    longitude=self.lon,
                    db_obj_list=None,
                ),
                status=status.HTTP_200_OK,
            )
        geometry__contains = f"POINT({self.lat} {self.lon})"
        sity =cast(str, city_data.get(f"city_{self.lang}") if city_data else city_data["city"])  # type: ignore
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
        return Response(
            GeoJsonSerializer(
                round_cords=self._get_rounded_coords(),
                sity=sity,
                db_obj_list=db_data,
                latitude=self.lat,
                longitude=self.lon,
            ),
            status=status.HTTP_200_OK,
        )

