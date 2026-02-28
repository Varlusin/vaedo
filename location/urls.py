from django.urls import path
from location.views import (
    FindLocationLonLat, 
    FindLocationTxt
   )

urlpatterns = [
    # path("orderedlocation/", user_order_adres),
    path("cordinats/", FindLocationLonLat.as_view(), name='findLocationByCordinats'),
    path("src/", FindLocationTxt.as_view(), name='findLocationByTxt'),
    # path('src/', search_location, name='src_loc'), 
    # path('adres/', src_loc ),
]