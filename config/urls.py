from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # Accounts URLs
    path("api/", include("accounts.routers")),

    # JWT Tokens
    path("api/", include("tokens.routers")),

    # Forex URLs
    path("api/", include("forex.routers")),

    # Metrics URL
    path("api/", include("metrics.routers")),
]
