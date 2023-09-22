from rest_framework import serializers

from forex.models import Currency, CurrencyPair, ForexOperation


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = "__all__"


class CurrencyPairSerializer(serializers.ModelSerializer):

    class Meta:
        model = CurrencyPair
        fields = "__all__"


class ForexOperationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ForexOperation
        fields = "__all__"