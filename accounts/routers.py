from django.urls import path

from accounts import views


urlpatterns = [
    # Users endpoints
    path("users", views.UserListView.as_view(), name="user-list"),
    path("users/current", views.CurrentUserView.as_view(), name="current-user"),
    path("users/<int:pk>", views.UserDetailView.as_view(), name="user-detail"),
]
