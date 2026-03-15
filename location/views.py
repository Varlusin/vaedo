# from django.db.models import F
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from location.models import CustomerAddresses, Building, Street
from location.serializers import LocationRequestSerializer, LocationSearchSerializer

from location.utils.coordinates import parse_coordinates
from location.utils.cordinaterequestdb import CreateResponceByValidLocationData

import asyncio


class FindLocationTxt(APIView):
    async def post(self, request) -> Response:
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

        # 1. Ստեղծում ենք Task-երը
        task_cord = asyncio.create_task(parse_coordinates(new_query))
        task_text = asyncio.create_task(self.process_text_search(new_query, old_query))

        # 2. Սպասում ենք առաջինն ավարտվածին
        done, pending = await asyncio.wait(
            [task_cord, task_text], return_when=asyncio.FIRST_COMPLETED
        )

        lang = request.LANGUAGE_CODE

        # ՍՏՈՒԳՈՒՄ 1: Եթե կորդինատների task-ն է ավարտվել (կամ երկուսն էլ)
        if task_cord in done:
            is_cord, data = task_cord.result() # Արդեն ավարտված է, await պետք չէ
            if is_cord:
                task_text.cancel() # Դադարեցնում ենք տեքստայինը
                resp_obj = CreateResponceByValidLocationData(validated_data=data, lang=lang)
                return resp_obj.create_responce() # Վերադարձնում է Response օբյեկտ
            
            # Եթե կորդինատ չէր, սպասում ենք տեքստայինին
            text_result = await task_text
            return Response(text_result)

        # ՍՏՈՒԳՈՒՄ 2: Եթե տեքստայինն է ավարտվել առաջինը
        else:
            # Քանի որ մեզ կորդինատն ավելի կարևոր է, սպասում ենք դրան
            is_cord, data = await task_cord
            if is_cord:
                resp_obj = CreateResponceByValidLocationData(validated_data=data, lang=lang)
                return resp_obj.create_responce()
            else:
                # Եթե կորդինատ չէր, վերցնում ենք արդեն ավարտված տեքստայինի արդյունքը
                text_result = task_text.result()
                return Response(text_result)

    async def process_text_search(self, n_qw: str, old_qw: str):
        # Սա վերադարձնում է dict, այլ ոչ թե Response
        return {"new_query": n_qw, "old_query": old_qw}
    








class FindLocationLonLat(APIView):
    def post(self, request) -> Response:
        serializer = LocationRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        lang = request.LANGUAGE_CODE
        resp = CreateResponceByValidLocationData(validated_data=serializer.validated_data, lang=lang)  # type: ignore
        return resp.create_responce()
