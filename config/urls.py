from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("accounts.routers")),
    path("api/", include("tokens.routers")),
    path("api/", include("assets.routers")),
    path("api/", include("trades.routers")),
]
