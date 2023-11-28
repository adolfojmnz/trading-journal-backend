from rest_framework.serializers import ModelSerializer, SerializerMethodField

from assets.models import Currency, CurrencyPair


class CurrencySerializer(ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"


class CurrencyPairSerializer(ModelSerializer):
    base_currency_symbol = SerializerMethodField()
    quote_currency_symbol = SerializerMethodField()

    def get_base_currency_symbol(self, currency_pair):
        return currency_pair.base_currency.symbol

    def get_quote_currency_symbol(self, currency_pair):
        return currency_pair.quote_currency.symbol

    class Meta:
        model = CurrencyPair
        fields = [
            "id",
            "symbol",
            "name",
            "base_currency",
            "base_currency_symbol",
            "quote_currency",
            "quote_currency_symbol",
            "pip_decimal_position",
        ]
