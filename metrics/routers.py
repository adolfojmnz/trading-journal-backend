from django.urls import path

from metrics.views import ForexMetricsView


urlpatterns = [
    path("metrics/forex", ForexMetricsView.as_view(), name="forex-metrics"),
]