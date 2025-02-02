from django.contrib import admin
from django.urls import path, include
from main.views import index

urlpatterns = [
    path("", index, name = 'home'),
    path("admin/", admin.site.urls),
    path('futur/', include('futur.urls'), name='futur'),
]
