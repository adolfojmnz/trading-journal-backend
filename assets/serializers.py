from rest_framework import serializers

from assets.models import Currency, CurrencyPair


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = "__all__"


class CurrencyPairSerializer(serializers.ModelSerializer):

    class Meta:
        model = CurrencyPair
        fields = "__all__"