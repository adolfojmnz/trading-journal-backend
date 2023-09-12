from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # Accounts URLs
    path("api/", include("accounts.api.routers")),

    # Assets URLs
    path("api/", include("assets.api.routers")),

    # Operations URLs
    path("api/", include("operations.api.routers")),
]
