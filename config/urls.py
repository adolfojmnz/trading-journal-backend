from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # Accounts URL
    path("api/", include("accounts.api.routers")),
]
