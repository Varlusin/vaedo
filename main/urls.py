from django.urls import path
from main.views import index, set_language


urlpatterns = [
    path("", index, name = 'home'),
    path('set-language/', set_language, name='set_language'),
]
