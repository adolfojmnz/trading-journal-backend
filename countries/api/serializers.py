from rest_framework.serializers import ModelSerializer

from countries.models import (
    Country,
    EconomicReport,
    EconomicIndicator,
)


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class EconomicIndicatorSerializer(ModelSerializer):
    class Meta:
        model = EconomicIndicator
        fields = "__all__"


class EconomicReportSerializer(ModelSerializer):
    class Meta:
        model = EconomicReport
        fields = "__all__"
