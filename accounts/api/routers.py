from django.urls import path
from django.utils import timezone

from rest_framework import status

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenBlacklistView,
    TokenObtainPairView,
)

from accounts.api import views
from accounts.models import User


class CustomTokenObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            user = User.objects.get(username=request.data['username'])
            user.last_login = timezone.now()
            user.save()
        return response


urlpatterns = [
    # JWT endpoints
    path('token', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist', TokenBlacklistView.as_view(), name='token_blacklist'),

    # Users endpoints
    path('users', views.UserListView.as_view(), name='user-list'),
    path('users/current', views.CurrentUserView.as_view(), name='current-user'),
    path('users/<int:pk>', views.UserDetailView.as_view(), name='user-detail'),

    # Trading Accounts endpoints
    path(
        "trading-accounts",
        views.TradingAccountListView.as_view(), name="trading-account-list",
    ),
    path(
        "trading-accounts/<int:pk>",
        views.TradingAccountDetailView.as_view(), name="trading-account-detail",
    ),

    # Trasactions endpoints
    path(
        "transactions",
        views.TransactionListView.as_view(), name="transaction-list",
    ),
    path(
        "transactions/<int:pk>",
        views.TransactionDetailView.as_view(), name="transaction-ddetail",
    ),
]
