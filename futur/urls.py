from django.urls import path
from futur.views import MainFuturList, FuturData
# from rest_framework import routers


urlpatterns = [
    path('', MainFuturList.as_view(), name='FuturList_root'),
    path(("<slug:slug>/"), FuturData.as_view(), name = 'FuturCategory_by_slug'),
]
