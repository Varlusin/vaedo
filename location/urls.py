from django.urls import path
from location.views import (
    FindLocationLonLat
   )

urlpatterns = [
    # path("orderedlocation/", user_order_adres),
    path("cordinats/", FindLocationLonLat.as_view(), name='findLocationByCordinats'),
    # path('src/', search_location, name='src_loc'), 
    # path('adres/', src_loc ),
]



