from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("accounts.routers")),
    path("api/", include("tokens.routers")),
    path("api/", include("assets.api.routers")),
    path("api/", include("trades.api.routers")),
    path("api/", include("metrics.api.routers.trades")),
]
