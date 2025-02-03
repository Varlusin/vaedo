from django.contrib import admin
from django.urls import path, include
from main.views import index
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path("admin/", admin.site.urls),

]


urlpatterns += i18n_patterns(
    path("i18n/", include("django.conf.urls.i18n")),
    path("", index, name = 'home'),
    path('futur/', include('futur.urls'), name='futur'),
    )