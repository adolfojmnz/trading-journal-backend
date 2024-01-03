from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)

from countries.models import (
    Country,
    EconomicReport,
    EconomicIndicator,
)


class CountrySerializer(ModelSerializer):
    currency_symbol = SerializerMethodField()

    def get_currency_symbol(self, country):
        return country.currency.symbol

    class Meta:
        model = Country
        fields = "__all__"


class EconomicIndicatorSerializer(ModelSerializer):
    country_code = SerializerMethodField()
    currency_symbol = SerializerMethodField()

    def get_country_code(self, indicator):
        return indicator.country.code

    def get_currency_symbol(self, indicator):
        return indicator.country.currency.symbol

    class Meta:
        model = EconomicIndicator
        fields = "__all__"


class EconomicReportSerializer(ModelSerializer):
    economic_indicator_name = SerializerMethodField()
    economic_indicator_country = SerializerMethodField()

    def get_economic_indicator_name(self, report):
        return report.economic_indicator.name

    def get_economic_indicator_country(self, report):
        return report.economic_indicator.country.code

    class Meta:
        model = EconomicReport
        fields = "__all__"
