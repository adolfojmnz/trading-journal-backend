from django.db.models import Sum, Max, Min, Avg, F, DurationField

from rest_framework.serializers import (
    Serializer,
    SerializerMethodField,
)


class TotalTradesMetrics:
    def get_total_trades(self, *args, **kwargs):
        return self.queryset.count()

    def get_total_profit_trades(self, *args, **kwargs):
        return self.queryset.filter(pnl__gt=0).count()

    def get_total_loss_trades(self, *args, **kwargs):
        return self.queryset.filter(pnl__lt=0).count()

    def get_total_short_trades(self, *args, **kwargs):
        return self.queryset.filter(type="S").count()

    def get_total_long_trades(self, *args, **kwargs):
        return self.queryset.filter(type="L").count()


class PNLMetrics:
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

    def get_largest_profit(self, *args, **kwargs):
        results = self.queryset.aggregate(
            Max("pnl")
        )["pnl__max"]
        return round(results or 0, 2)

    def get_largest_loss(self, *args, **kwargs):
        results = self.queryset.aggregate(Min("pnl"))["pnl__min"]
        return round(results or 0, 2)

    def get_smallest_profit(self, *args, **kwargs):
        results = self.queryset.filter(pnl__gt=0).aggregate(
            Min("pnl")
        )["pnl__min"]
        return round(results or 0, 2)

    def get_smallest_loss(self, *args, **kwargs):
        results = self.queryset.filter(pnl__lt=0).aggregate(
            Max("pnl")
        )["pnl__max"]
        return round(results or 0, 2)

    def get_avg_profit_per_trade(self, *args, **kwargs):
        results = self.queryset.filter(pnl__gt=0).aggregate(
            Avg("pnl")
        )["pnl__avg"]
        return round(results or 0, 2)

    def get_avg_loss_per_trade(self, *args, **kwargs):
        results = self.queryset.filter(pnl__lt=0).aggregate(
            Avg("pnl")
        )["pnl__avg"]
        return round(results or 0, 2)


class HoldingTimeMetrics:
    def get_avg_holding_time(self, *args, queryset=None, **kwargs):
        queryset = queryset or self.queryset
        if not queryset.count():
            return round(0, 2)
        average_holding_time = queryset.aggregate(
            average_holding_time=Avg(
                F("close_datetime") - F("open_datetime"),
                output_field=DurationField(),
            )
        )["average_holding_time"]
        return round(average_holding_time.total_seconds(), 2)

    def get_avg_holding_time_per_long_trade(self, *args, **kwargs):
        return self.get_avg_holding_time(self.queryset.filter(type="L"))

    def get_avg_holding_time_per_short_trade(self, *args, **kwargs):
        return self.get_avg_holding_time(self.queryset.filter(type="S"))

    def get_avg_holding_time_per_profit_trade(self, *args, **kwargs):
        return self.get_avg_holding_time(
            self.queryset.filter(pnl__gt=0)
        )

    def get_avg_holding_time_per_loss_trade(self, *args, **kwargs):
        return self.get_avg_holding_time(
            self.queryset.filter(pnl__lt=0)
        )


class AssetMetricsSerializer(TotalTradesMetrics,
                             PNLMetrics,
                             HoldingTimeMetrics,
                             Serializer):
    total_trades = SerializerMethodField()
    total_profit_trades = SerializerMethodField()
    total_loss_trades = SerializerMethodField()
    total_short_trades = SerializerMethodField()
    total_long_trades = SerializerMethodField()
    net_profit = SerializerMethodField()
    gross_profit = SerializerMethodField()
    gross_loss = SerializerMethodField()
    largest_loss = SerializerMethodField()
    largest_profit = SerializerMethodField()
    avg_profit_per_trade = SerializerMethodField()
    avg_loss_per_trade = SerializerMethodField()
    avg_holding_time = SerializerMethodField()
    avg_holding_time_per_long_trade = SerializerMethodField()
    avg_holding_time_per_short_trade = SerializerMethodField()
    avg_holding_time_per_profit_trade = SerializerMethodField()
    avg_holding_time_per_loss_trade = SerializerMethodField()

    def __init__(self, queryset, *args, **kwargs):
        self.queryset = queryset
        return super().__init__(*args, **kwargs)

    class Meta:
        fields = [
            "total_trades",
            "total_profit_trades",
            "total_loss_trades",
            "total_short_trades",
            "total_long_trades",
            "net_profit",
            "gross_profit",
            "gross_loss",
            "largest_profit",
            "largest_loss",
            "avg_profit_per_trade",
            "avg_loss_per_trade",
            "avg_holding_time",
            "avg_holding_time_per_long_trade",
            "avg_holding_time_per_short_trade",
            "avg_holding_time_per_profit_trade",
            "avg_holding_time_per_loss_trade",
        ]
