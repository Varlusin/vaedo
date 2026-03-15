# from django.db.models import F
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from location.models import CustomerAddresses, Building, Street
from location.serializers import LocationRequestSerializer, LocationSearchSerializer

from location.utils.coordinates import parse_coordinates
from location.utils.cordinaterequestdb import CreateResponceByValidLocationData
from location.utils.geojsonrender import GEOJSONRender

from TextProcessing import _unicodelowersplit as uls

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

import time

from pprint import pprint


class FindLocationTxt(APIView):
    def post(self, request) -> Response:
        start_time = time.time()
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

        with ThreadPoolExecutor(max_workers=2) as ex:
            future_map = {
                ex.submit(check_cord, new_query): "cord",
                ex.submit(primary_processing, new_query): "primary_processing",
            }
        paralel_rezults = {}
        for future in as_completed(future_map):
            result = future.result()
            source = future_map[future]
            paralel_rezults[source] = result

        if paralel_rezults["cord"] is not None:
            return Response(
                data={
                    "adr": GEOJSONRender(**paralel_rezults["cord"]),
                    "time": (time.time() - start_time) * 1000,
                },
                status=status.HTTP_200_OK,
            )
        return Response({"type": new_query, "time": (time.time() - start_time) * 1000})


def primary_processing(txt: str):
    quetr_token = uls(txt)
    print(quetr_token)


def check_cord(txt: str, lang="en"):
    is_cord, data = parse_coordinates(txt)
    if is_cord:
        resp = CreateResponceByValidLocationData(validated_data=data, lang=lang)
        rezult_ = resp.create_responce()
        return rezult_
    return None


def adres_search(txt: str, lang="en"):
    return {
        "type": "adres_search",
    }


def spetial_adres_search(txt: str, lang="en"):
    return {
        "type": "spetial_adres_search",
    }


class FindLocationLonLat(APIView):
    def post(self, request) -> Response:
        serializer = LocationRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        lang = request.LANGUAGE_CODE
        resp = CreateResponceByValidLocationData(validated_data=serializer.validated_data, lang=lang)  # type: ignore
        rezult_ = resp.create_responce()
        return Response(
            data=GEOJSONRender(**rezult_),
            status=status.HTTP_200_OK,
        )
