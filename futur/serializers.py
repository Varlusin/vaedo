from futur.models import Typefutur, Futur
from rest_framework import serializers



class MainFuturSerializers(serializers.ModelSerializer):
    class Meta:
        model = Futur
        fields = ("names", "slug", "url")


class MainFuturPrefatchSerializers(serializers.ModelSerializer):
    futur = MainFuturSerializers(many=True, read_only=True)  # Prefetched data

    class Meta:
        model = Typefutur
        fields = ("slug", "futurtype", "futur")
    def get_futur(self, obj):
        """
        This ensures the pre-fetched `futur` objects are serialized efficiently
        without triggering N+1 queries.
        """
        futur_queryset = obj.futur.all()  # Access the prefetched futur objects
        return MainFuturSerializers(futur_queryset, many=True).data


class FuturSerializers(serializers.ModelSerializer):
    class Meta:
        model = Futur
        fields = ("slug", "names", "descriptions", "img")