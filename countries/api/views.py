from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    SAFE_METHODS,
)
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateAPIView,
)

from countries.models import (
    Country,
    EconomicReport,
    EconomicIndicator,
)
from countries.api.serializers import (
    CountrySerializer,
    EconomicReportSerializer,
    EconomicIndicatorSerializer,
)


class PermisionsMixin:
    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        if self.request.method not in SAFE_METHODS:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class CountryListView(PermisionsMixin, ListCreateAPIView):
    model = Country
    queryset = model.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticated]


class CountryDetailView(PermisionsMixin, RetrieveUpdateAPIView):
    model = Country
    queryset = model.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticated]


class EconomicIndicatorListView(PermisionsMixin, ListCreateAPIView):
    model = EconomicIndicator
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = EconomicIndicatorSerializer


class EconomicIndicatorDetailView(PermisionsMixin, RetrieveUpdateAPIView):
    model = EconomicIndicator
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = EconomicIndicatorSerializer


class EconomicReportListView(PermisionsMixin, ListCreateAPIView):
    model = EconomicReport
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = EconomicReportSerializer


class EconomicReportDetailView(PermisionsMixin, RetrieveUpdateAPIView):
    model = EconomicReport
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = EconomicReportSerializer
