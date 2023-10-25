from django.db.models import Sum, Max, Min, Avg, F, DurationField

from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    SerializerMethodField,
)

from trades.models import Trade


class TradeMetricsMixin:

    def get_average_holding_time(self, queryset=None) -> float:
        if not queryset.count():
            return 0.0
        average_holding_time = queryset.aggregate(
            average_holding_time=Avg(
                F('close_datetime') - F('open_datetime'),
                output_field=DurationField()
            )
        )['average_holding_time']
        return round(average_holding_time.total_seconds(), 2)


class TradeSerializer(ModelSerializer):

    class Meta:
        model = Trade
        fields = "__all__"


class TradeMetricsSerializer(TradeMetricsMixin, Serializer):
    net_profit = SerializerMethodField()
    gross_profit = SerializerMethodField()
    gross_loss = SerializerMethodField()
    total_trades = SerializerMethodField()
    total_profit_trades = SerializerMethodField()
    total_loss_trades = SerializerMethodField()
    largest_profit_trade = SerializerMethodField()
    largest_loss_trade = SerializerMethodField()
    average_profit_trade = SerializerMethodField()
    average_loss_trade = SerializerMethodField()
    percentage_profit_trades = SerializerMethodField()
    percentage_loss_trades = SerializerMethodField()
    total_long_positions = SerializerMethodField()
    total_short_positions = SerializerMethodField()
    average_holding_time = SerializerMethodField()
    average_holding_time_per_winning_trade = SerializerMethodField()
    average_holding_time_per_lossing_trade = SerializerMethodField()
    average_holding_time_per_long_position = SerializerMethodField()
    average_holding_time_per_short_position = SerializerMethodField()

    def __init__(self, queryset=None, *args, **kwargs):
        self.queryset = queryset
        return super().__init__(*args, **kwargs)

    def get_net_profit(self, *args, **kwargs):
        results = self.queryset.aggregate(Sum("pnl"))["pnl__sum"]
        return round(results or 0, 2)

    def get_gross_profit(self, *args, **kwargs):
        results = self.queryset.filter(pnl__gt=0).aggregate(
            Sum("pnl")
        )["pnl__sum"]
        return round(results or 0, 2)

    def get_gross_loss(self, *args, **kwargs):
        results = self.queryset.filter(pnl__lt=0).aggregate(
            Sum("pnl")
        )["pnl__sum"]
        return round(results or 0, 2)

    def get_total_trades(self, *args, **kwargs):
        results = self.queryset.count()
        return results or 0

    def get_total_profit_trades(self, *args, **kwargs):
        results = self.queryset.filter(pnl__gt=0).count()
        return results or 0

    def get_total_loss_trades(self, *args, **kwargs):
        results = self.queryset.filter(pnl__lt=0).count()
        return results or 0

    def get_largest_profit_trade(self, *args, **kwargs):
        results = self.queryset.aggregate(Max("pnl"))["pnl__max"]
        return round(results or 0, 2)

    def get_largest_loss_trade(self, *args, **kwargs):
        results = self.queryset.aggregate(Min("pnl"))["pnl__min"]
        return round(results or 0, 2)

    def get_average_profit_trade(self, *args, **kwargs):
        results = self.queryset.filter(
            pnl__gt=0
        ).aggregate(Avg("pnl"))["pnl__avg"]
        return round(results or 0, 2)

    def get_average_loss_trade(self, *args, **kwargs):
        results = self.queryset.filter(
            pnl__lt=0
        ).aggregate(Avg("pnl"))["pnl__avg"]
        return round(results or 0, 2)

    def get_percentage_profit_trades(self, *args, **kwargs):
        total_trades = self.queryset.count()
        profit_trades = self.queryset.filter(pnl__gt=0).count()
        if not profit_trades or not total_trades:
            return 0.00
        results = (profit_trades/total_trades) * 100
        return round(results, 2)

    def get_percentage_loss_trades(self, *args, **kwargs):
        total_trades = self.queryset.count()
        loss_trades = self.queryset.filter(pnl__lt=0).count()
        if not total_trades or not loss_trades:
            return 0.00
        results = (loss_trades/total_trades) * 100
        return round(results, 2)

    def get_total_short_positions(self, *args, **kwargs):
        results = self.queryset.filter(type="S").count()
        return results or 0

    def get_total_long_positions(self, *args, **kwargs):
        results = self.queryset.filter(type="L").count()
        return results or 0

    def get_average_holding_time(self, *args, **kwargs):
        """ Returns the average holding time of all trades in the queryset.
            Output: average holding time in in seconds.
        """
        return super().get_average_holding_time(self.queryset)

    def get_average_holding_time_per_winning_trade(self, *args, **kwargs):
        """ Returns the average holding time for all trades with profits.
            Output: average holding time in in seconds.
        """
        return super().get_average_holding_time(self.queryset.filter(pnl__gt=0))

    def get_average_holding_time_per_lossing_trade(self, *args, **kwargs):
        """ Returns the average holding time for all trades with losses.
            Output: average holding time in in seconds.
        """
        return super().get_average_holding_time(self.queryset.filter(pnl__lt=0))

    def get_average_holding_time_per_long_position(self, *args, **kwargs):
        """ Returns the average holding time for all long position trades.
            Output: average holding time in in seconds.
        """
        return super().get_average_holding_time(self.queryset.filter(type="L"))

    def get_average_holding_time_per_short_position(self, *args, **kwargs) -> float:
        """ Returns the average holding time for all short position trades.
            Output: average holding time in in seconds.
        """
        return super().get_average_holding_time(self.queryset.filter(type="S"))

    class Meta:
        fields = [
            "net_profit",
            "gross_profit",
            "gross_loss",
            "total_trades",
            "total_profit_trades",
            "total_loss_trades",
            "largest_profit_trade",
            "largest_loss_trade",
            "average_profit_trade",
            "average_loss_trade",
            "percentage_profit_trades",
            "percentage_loss_trades",
            "total_long_positions",
            "total_short_positions",
            "average_holding_time",
            "average_holding_time_per_winning_trade",
            "average_holding_time_per_lossing_trade",
            "average_holding_time_per_long_position",
            "average_holding_time_per_short_position",
        ]