from futur.models import Typefutur, Futur
from rest_framework import serializers



class MainFuturSerializers(serializers.ModelSerializer):
    class Meta:
        model = Futur
        fields = ("names", "url")


class MainFuturPrefatchSerializers(serializers.ModelSerializer):
    futur = MainFuturSerializers(many=True, read_only=True)  # Prefetched data

    class Meta:
        model = Typefutur
        fields = ("futurtype", "futur")
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
        fields = ("names", "descriptions", "img")