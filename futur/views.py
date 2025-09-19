from django.db.models import Prefetch
from django.utils.translation import get_language
from django.http import Http404

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from futur.models import Typefutur, Futur

from futur.serializers import MainFuturPrefatchSerializers, FuturSerializers

class MainFuturList(generics.ListAPIView):
    serializer_class = MainFuturPrefatchSerializers

    def get_queryset(self):
        language = get_language()
        futur_queryset = (
            Futur.objects.published()
            .with_translations(language=language, fields=['names', 'url', 'category_id'])
            )

        return (
            Typefutur.objects.published()
            .with_translations(language=language, fields=["futurtype"])
            .prefetch_related(Prefetch("futur", queryset=futur_queryset))
        )



class FuturData(APIView):
    def get_object(self, slug):
        try:
            language = get_language()
            return (
                Futur.objects.published()
                .with_translations(language=language,fields=["names","slug","descriptions","img"])
                .get(slug=slug)
            )
        except Futur.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        futur_query = self.get_object(slug)
        serializer = FuturSerializers(futur_query)
        return Response(serializer.data)


