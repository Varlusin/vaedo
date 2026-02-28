from django.db.models import F
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from location.models import CustomerAddresses, Building, Street
from location.serializers import LocationRequestSerializer, LocationSearchSerializer
from location.utils.utils import create_responce


class FindLocationTxt(APIView):
    def post(self, request):
        serializer = LocationSearchSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )


        new_query = serializer.validated_data["query"]
        old_query = request.session.get("last_query", "")
        request.session["last_query"] = new_query

        # Քո հիմնական տրամաբանությունը
        return Response({"type": new_query, "old_query": old_query})


class FindLocationLonLat(APIView):
    def post(self, request):
        serializer = LocationRequestSerializer(data=request.data)
        lang = request.LANGUAGE_CODE

        if not serializer.is_valid():
            return Response(
                {"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        is_ok, request_data = serializer.get_request_data(lang)

        if not is_ok:
            return Response(
                create_responce(
                    serializer.get_rounded_coords(),
                    request_data,
                    db_obj_list=None,
                    latitude=serializer.validated_data["latitude"],
                    longitude=serializer.validated_data["longitude"],
                ),
                status=status.HTTP_200_OK,
            )

        qs = Building.objects.select_related("stret").filter(
            sity_id=request_data["sity_id"]
        )

        if request_data["district"]:
            qs = qs.filter(district=request_data["district"])

        qs = qs.filter(geometry__contains=request_data["geometry__contains"]).values(
            building=F("id"), adr=F("adres"), street=F(f"stret__name_{lang}")
        )

        db_data = next(iter(qs), None)

        return Response(
            create_responce(
                serializer.get_rounded_coords(),
                request_data["sity"],
                db_obj_list=db_data,
                latitude=serializer.validated_data["latitude"],
                longitude=serializer.validated_data["longitude"],
            ),
            status=status.HTTP_200_OK,
        )
