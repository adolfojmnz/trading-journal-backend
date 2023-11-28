from django.urls import path

from accounts.api.views import (
    UserListView,
    CurrentUserView,
    UserDetailView,
)


urlpatterns = [
    # Users endpoints
    path("users", UserListView.as_view(), name="user-list"),
    path("users/current", CurrentUserView.as_view(), name="current-user"),
    path("users/<int:pk>", UserDetailView.as_view(), name="user-detail"),
]
