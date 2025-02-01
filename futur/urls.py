from django.urls import path
from futur.views import MainFuturList, FuturCategory
# from rest_framework import routers


urlpatterns = [
    path('', MainFuturList.as_view(), name='FuturList_root'),
    path(("<int:pk>/"), FuturCategory.as_view(), name = 'FuturCategory_by_slug'),
]
