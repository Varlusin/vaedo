from rest_framework import serializers
from shapely.geometry import Point as ShapelyPoint
from django.utils.translation import gettext_lazy as _

from location.spatial_service import spatial_service, SASC

class LocationSearchSerializer(serializers.Serializer):
    query = serializers.CharField(min_length=3, required=True)
    
    def validate(self, data,):
        data["query"] =  data["query"].lower()
        return data


class LocationRequestSerializer(serializers.Serializer):
    latitude = serializers.FloatField(min_value=-90, max_value=90)
    longitude = serializers.FloatField(min_value=-180, max_value=180)

    def validate(self, data):
        latitude = data["latitude"]
        longitude = data["longitude"]
        point = ShapelyPoint(latitude, longitude)

        if not SASC._check_cord(lat=latitude, lng= longitude):
            raise serializers.ValidationError(_("Service not available in this area"))

        if not spatial_service.check_avelable(point=point):
            raise serializers.ValidationError(
                _("Service not available at this location")
            )

        data["point"] = point
        return data
