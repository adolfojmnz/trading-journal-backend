from django.urls import path

from metrics.api.views.assets import AssetMetricsView


urlpatterns = [
    path(
        "assets/<int:pk>/metrics",
        AssetMetricsView.as_view(),
        name="asset-metrics",
    ),
]
