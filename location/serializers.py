from rest_framework import serializers
from shapely.geometry import Point as ShapelyPoint
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache

SERVICE_AVAILABLE_SPACE = cache.get("SERVICE_AVAILABLE_SPACE")
SITY_LIST = cache.get("SITY_LIST")
COMUNITY_DATA = cache.get("COMUNITY_DATA")


class LocationRequestSerializer(serializers.Serializer):
    latitude = serializers.CharField()
    longitude = serializers.CharField()
    
    def validate(self, data):
        try:
            latitude = float(data['latitude'])
            longitude = float(data['longitude'])
        except (ValueError, TypeError):
            raise serializers.ValidationError(_("Invalid coordinates"))

        point = ShapelyPoint(latitude, longitude)
        if not (43.76 <= latitude <= 43.9264) or not (40.706 <= longitude <= 40.855):
            raise serializers.ValidationError(_("Service not available in this area"))

        if not SERVICE_AVAILABLE_SPACE or not point.within(SERVICE_AVAILABLE_SPACE):
            raise serializers.ValidationError(_("Service not available at this location"))

        data['lat'] = latitude
        data['lon'] = longitude
        data['point'] = point
        return data

    def get_request_data(self, lang):
        """Returns sity/community info from cache based on validated data"""
        point = self.validated_data['point']

        sity_data = next(
            (
                {
                    "sity": sity.get(f"sity_{lang}"),
                    "id": sity["id"]
                }
                for sity in SITY_LIST
                if point.within(sity["geometry"])
            ),
            None
        )

        if not sity_data:
            return False, _("Shirak region")

        if sity_data["id"] == 1:
            sity_data["community_id"] = next(
                (
                    community["id"]
                    for community in COMUNITY_DATA
                    if point.within(community["geometry"])
                ),
                None
            )

        return True, {
            "sity_id": sity_data["id"],
            "district": sity_data.get("community_id"),
            "geometry__contains": f'POINT({self.validated_data["lat"]} {self.validated_data["lon"]})',
            "sity": sity_data["sity"]
        }

    def get_rounded_coords(self, digits=4):
        return f'{round(self.validated_data["lon"], digits)} {round(self.validated_data["lat"], digits)}'






