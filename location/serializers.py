from rest_framework import serializers
from shapely.geometry import Point as ShapelyPoint
from django.utils.translation import gettext_lazy as _

from location.spatial_service import spatial_service

min_lat, max_lat, min_lon, max_lon = 43.76, 43.9264, 40.706, 40.855


class LocationSearchSerializer(serializers.Serializer):
    query = serializers.CharField(min_length=3, required=True)


class LocationRequestSerializer(serializers.Serializer):
    latitude = serializers.FloatField(min_value=-90, max_value=90)
    longitude = serializers.FloatField(min_value=-180, max_value=180)

    def validate(self, data):
        latitude = data["latitude"]
        longitude = data["longitude"]
        point = ShapelyPoint(latitude, longitude)

        if not (min_lat <= latitude <= max_lat and min_lon <= longitude <= max_lon):
            raise serializers.ValidationError(_("Service not available in this area"))

        if not spatial_service.check_avelable(point=point):
            raise serializers.ValidationError(
                _("Service not available at this location")
            )

        data["point"] = point
        return data

    def get_request_data(self, lang):
        point = self.validated_data["point"]
        lat = self.validated_data["latitude"]
        lon = self.validated_data["longitude"]
        city_id, city_data = spatial_service.find_city(point=point)

        if not city_id:
            return False, _("Shirak region")

        district = None
        if city_id == 1:
            district = spatial_service.find_district(point=point)

        return True, {
            "sity_id": city_id,
            "district": district,
            "geometry__contains": f"POINT({lat} {lon})",
            "sity": city_data.get(f"city_{lang}"),
        }

    def get_rounded_coords(self, digits=4):
        return f'{round(self.validated_data["longitude"], digits)} {round(self.validated_data["latitude"], digits)}'
