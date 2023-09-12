from django.urls import path

from operations.api import views


urlpatterns = [
    path(
        "operations/forex",
        views.ForexOperationListView.as_view(), name="forex-operation-list",
    ),
    path(
        "operations/forex/<int:pk>",
        views.ForexOperationDetailView.as_view(), name="forex-operation-detail",
    ),
]