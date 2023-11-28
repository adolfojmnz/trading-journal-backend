from rest_framework.serializers import ModelSerializer, SerializerMethodField

from trades.models import Trade


class TradeSerializer(ModelSerializer):
    currency_pair_symbol = SerializerMethodField()

    def get_currency_pair_symbol(self, trade):
        return trade.currency_pair.symbol

    class Meta:
        model = Trade
        fields = [
            "id",
            "ticket",
            "type",
            "currency_pair",
            "currency_pair_symbol",
            "open_datetime",
            "close_datetime",
            "open_price",
            "stop_loss",
            "take_profit",
            "close_price",
            "volume",
            "pnl",
        ]
