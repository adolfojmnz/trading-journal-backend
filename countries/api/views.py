from rest_framework.permissions import IsAuthenticated
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


class CountryListView(ListCreateAPIView):
    model = Country
    queryset = model.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticated]


class CountryDetailView(RetrieveUpdateAPIView):
    model = Country
    queryset = model.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticated]


class EconomicIndicatorListView(ListCreateAPIView):
    model = EconomicIndicator
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = EconomicIndicatorSerializer


class EconomicIndicatorDetailView(RetrieveUpdateAPIView):
    model = EconomicIndicator
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = EconomicIndicatorSerializer


class EconomicReportListView(ListCreateAPIView):
    model = EconomicReport
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = EconomicReportSerializer


class EconomicReportDetailView(RetrieveUpdateAPIView):
    model = EconomicReport
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = EconomicReportSerializer
