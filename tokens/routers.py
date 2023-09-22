from django.urls import path

from rest_framework_simplejwt.views import (
    TokenVerifyView,
    TokenRefreshView,
    TokenBlacklistView,
)

from tokens.views import CustomTokenObtainPairView


urlpatterns = [
    path("token", CustomTokenObtainPairView.as_view(), name="token-pair"),
    path("token/verify", TokenVerifyView.as_view(), name="token-verify"),
    path("token/refresh", TokenRefreshView.as_view(), name="token-refresh"),
    path("token/blacklist", TokenBlacklistView.as_view(), name="token-blacklist"),
]
