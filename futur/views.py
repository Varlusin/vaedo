from django.db.models import Prefetch
from django.utils.translation import get_language
from rest_framework import generics

from futur.models import Typefutur, Futur

from futur.serializers import MainFuturPrefatchSerializers, FuturSerializers

# from rest_framework.viewsets import ReadOnlyModelViewSet


from django.db import connection
from pprint import pprint

class MainFuturList(generics.ListAPIView):
    serializer_class = MainFuturPrefatchSerializers

    def get_queryset(self):
        lang = get_language()
        futurtype_field = f"futurtype_{lang}"
        names_field = f"names_{lang}"

        futur_queryset = Futur.objects.published().only(
            names_field,"url", "slug", "category_id"
        )

        return (
            Typefutur.objects.published()
            .only(futurtype_field, "slug")  # Only load fields for Typefutur
            .prefetch_related(Prefetch("futur", queryset=futur_queryset))
        )

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        print(connection.queries)
        return response


class FuturCategory(generics.RetrieveAPIView):
    queryset = Futur.objects.all()
    serializer_class = FuturSerializers
