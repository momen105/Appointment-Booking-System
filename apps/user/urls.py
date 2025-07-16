from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='access_token'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='refresh_token'),
]
