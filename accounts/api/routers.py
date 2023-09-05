from django.urls import path

from accounts.api import views


urlpatterns = [
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
