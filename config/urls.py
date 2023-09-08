from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # Accounts URLs
    path("api/", include("accounts.api.routers")),

    # Currency URLs
    path("api/", include("currency.api.routers")),
]
