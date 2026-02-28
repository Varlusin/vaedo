from django.urls import path, include

from rest_framework_simplejwt.views import TokenVerifyView
from accaunts.views import (
    RegisterViewset, 
    CustomTokenObtainPairView, 
    CustomTokenRefreshView,
    GetprofileView,
)

urlpatterns = [
    path('registration/', RegisterViewset.as_view({'post': 'create', 'get': 'list'}), name='registration'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('profile/', GetprofileView.as_view(), name='get_profile'),
]
