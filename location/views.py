
# from django.db.models import F
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from location.models import CustomerAddresses, Building, Street
from location.serializers import LocationRequestSerializer, LocationSearchSerializer

from location.utils.coordinates import parse_coordinates
from location.utils.cordinaterequestdb import  CreateResponceByValidLocationData





class FindLocationTxt(APIView):
    def post(self, request)->Response:
        serializer = LocationSearchSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        new_query = serializer.validated_data["query"]
        old_query = request.session.get("last_query", "")
        if new_query == old_query:
            return Response(
                {"warning": _("the query is the same")},
                status=status.HTTP_200_OK,
            )
        request.session["last_query"] = new_query

        is_cord, data = parse_coordinates(new_query)

        if is_cord:
            lang = request.LANGUAGE_CODE
            resp = CreateResponceByValidLocationData(validated_data= data, lang=lang)
            return resp.create_responce()
            

        return Response({"type": new_query, "old_query": old_query, "is_cord": is_cord})





class FindLocationLonLat(APIView):
    def post(self, request)->Response:
        serializer = LocationRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        lang = request.LANGUAGE_CODE
        resp = CreateResponceByValidLocationData(validated_data=serializer.validated_data, lang=lang) # type: ignore
        return resp.create_responce()
        
