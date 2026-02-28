from django.urls import path, include

urlpatterns = [
    path("", include('main.urls'), name='home'),
    path('futur/', include('futur.urls'), name='futur'),
    path('accaunts/', include('accaunts.urls'), name='accaunts'),
    path('location/', include('location.urls'), name = 'location'),

]

