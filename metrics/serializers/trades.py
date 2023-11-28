from django.db.models import Sum, Max, Min, Avg, F, DurationField

from rest_framework.serializers import (
    Serializer,
    SerializerMethodField,
)


class MetricsSerializerMixin(Serializer):
    def __init__(self, queryset, *args, **kwargs):
        self.queryset = queryset
        return super().__init__(*args, **kwargs)


class GetPNLMetrics:
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

    def get_average_profit(self, *args, **kwargs):
        results = self.queryset.filter(pnl__gt=0).aggregate(
            Avg("pnl")
        )["pnl__avg"]
        return round(results or 0, 2)

    def get_average_loss(self, *args, **kwargs):
        results = self.queryset.filter(pnl__lt=0).aggregate(
            Avg("pnl")
        )["pnl__avg"]
        return round(results or 0, 2)

    def get_profit_loss_ratio(self, *args, **kwargs):
        total_trades = self.queryset.count()
        profit_trades = self.queryset.filter(pnl__gt=0).count()
        if not profit_trades or not total_trades:
            return 0.00
        results = (profit_trades / total_trades)
        return round(results, 2)

    def get_loss_profit_ratio(self, *args, **kwargs):
        total_trades = self.queryset.count()
        loss_trades = self.queryset.filter(pnl__lt=0).count()
        if not total_trades or not loss_trades:
            return 0.00
        results = (loss_trades / total_trades)
        return round(results, 2)


class GetTotalTradesMetrics:
    def get_total_trades(self, *args, **kwargs):
        return self.queryset.count()

    def get_total_profit_trades(self, *args, **kwargs):
        return self.queryset.filter(pnl__gt=0).count()

    def get_total_loss_trades(self, *args, **kwargs):
        return self.queryset.filter(pnl__lt=0).count()

    def get_total_short_positions(self, *args, **kwargs):
        return self.queryset.filter(type="S").count()

    def get_total_long_positions(self, *args, **kwargs):
        return self.queryset.filter(type="L").count()


class GetHoldingTimeMetrics:
    def get_average_holding_time(self, *args, queryset=None, **kwargs):
        """Returns the average holding time of all trades in the queryset.
        Output: average holding time in in seconds.
        """
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

    def get_average_holding_time_per_winning_trade(self, *args, **kwargs):
        """Returns the average holding time for all trades with profits.
        Output: average holding time in in seconds.
        """
        return self.get_average_holding_time(
            self.queryset.filter(pnl__gt=0)
        )

    def get_average_holding_time_per_lossing_trade(self, *args, **kwargs):
        """Returns the average holding time for all trades with losses.
        Output: average holding time in in seconds.
        """
        return self.get_average_holding_time(
            self.queryset.filter(pnl__lt=0)
        )

    def get_average_holding_time_per_long_position(self, *args, **kwargs):
        """Returns the average holding time for all long position trades.
        Output: average holding time in in seconds.
        """
        return self.get_average_holding_time(self.queryset.filter(type="L"))

    def get_average_holding_time_per_short_position(self, *args, **kwargs):
        """Returns the average holding time for all short position trades.
        Output: average holding time in in seconds.
        """
        return self.get_average_holding_time(self.queryset.filter(type="S"))


class GetPositionVolume:
    def get_min_position_volume(self, *args, **kwargs):
        return self.queryset.aggregate(Min("volume"))["volume__min"] or 0

    def get_max_position_volume(self, *args, **kwargs):
        return self.queryset.aggregate(Max("volume"))["volume__max"] or 0

    def get_min_position_volume_per_winning_trade(self, *args, **kwargs):
        return self.queryset.filter(pnl__gt=0).aggregate(
            Min("volume")
        )["volume__min"] or 0

    def get_min_position_volume_per_losing_trade(self, *args, **kwargs):
        return self.queryset.filter(pnl__lt=0).aggregate(
            Min("volume")
        )["volume__min"] or 0

    def get_max_position_volume_per_winning_trade(self, *args, **kwargs):
        return self.queryset.filter(pnl__gt=0).aggregate(
            Max("volume")
        )["volume__max"] or 0

    def get_max_position_volume_per_losing_trade(self, *args, **kwargs):
        return self.queryset.filter(pnl__lt=0).aggregate(
            Max("volume")
        )["volume__max"] or 0

    def get_average_position_volume(self, *args, **kwargs):
        results = self.queryset.aggregate(
            Avg("volume")
        )["volume__avg"]
        return round(results or 0, 2)

    def get_average_position_volume_per_winning_trade(self, *args, **kwargs):
        results = self.queryset.filter(pnl__gt=0).aggregate(Avg("volume"))[
            "volume__avg"
        ]
        return round(results or 0, 2)

    def get_average_position_volume_per_losing_trade(self, *args, **kwargs):
        results = self.queryset.filter(pnl__lt=0).aggregate(Avg("volume"))[
            "volume__avg"
        ]
        return round(results or 0, 2)

    def get_average_position_volume_per_long_position(self, *args, **kwargs):
        results = self.queryset.filter(type="L").aggregate(
            Avg("volume")
        )["volume__avg"]
        return round(results or 0, 2)

    def get_average_position_volume_per_short_position(self, *args, **kwargs):
        results = self.queryset.filter(type="S").aggregate(
            Avg("volume")
        )["volume__avg"]
        return round(results or 0, 2)


class MetricsSummarySerializer(MetricsSerializerMixin,
                               GetPNLMetrics,
                               GetTotalTradesMetrics,
                               GetHoldingTimeMetrics,
                               GetPositionVolume):
    total_trades = SerializerMethodField()
    total_profit_trades = SerializerMethodField()
    total_loss_trades = SerializerMethodField()
    net_profit = SerializerMethodField()
    gross_profit = SerializerMethodField()
    gross_loss = SerializerMethodField()
    average_profit = SerializerMethodField()
    average_loss = SerializerMethodField()
    profit_loss_ratio = SerializerMethodField()
    loss_profit_ratio = SerializerMethodField()
    average_holding_time = SerializerMethodField()
    average_position_volume = SerializerMethodField()

    class Meta:
        fields = [
            "total_trades",
            "total_profit_trades",
            "total_loss_trades",
            "net_profit",
            "gross_profit",
            "gross_loss",
            "average_profit_trade",
            "average_loss_trade",
            "profit_loss_ratio",
            "loss_profit_ratio",
            "average_holding_time",
            "average_position_volume",
        ]


class ProfitAndLossSerializer(MetricsSerializerMixin, GetPNLMetrics):
    net_profit = SerializerMethodField()
    gross_profit = SerializerMethodField()
    gross_loss = SerializerMethodField()
    largest_profit = SerializerMethodField()
    largest_loss = SerializerMethodField()
    smallest_profit = SerializerMethodField()
    smallest_loss = SerializerMethodField()
    average_profit = SerializerMethodField()
    average_loss = SerializerMethodField()
    profit_loss_ratio = SerializerMethodField()
    loss_profit_ratio = SerializerMethodField()

    class Meta:
        fields = [
            "net_profit",
            "gross_profit",
            "gross_loss",
            "largest_profit",
            "largest_loss",
            "smallest_profit",
            "smallest_loss",
            "average_profit",
            "average_loss",
            "profit_loss_ratio",
            "loss_profit_ratio",
        ]


class TotalTradesSerializer(MetricsSerializerMixin, GetTotalTradesMetrics):
    total_trades = SerializerMethodField()
    total_profit_trades = SerializerMethodField()
    total_loss_trades = SerializerMethodField()
    total_long_positions = SerializerMethodField()
    total_short_positions = SerializerMethodField()

    class Meta:
        fields = [
            "total_trades",
            "total_profit_trades",
            "total_loss_trades",
            "total_long_positions",
            "total_short_positions",
        ]


class HoldingTimeSerializer(MetricsSerializerMixin, GetHoldingTimeMetrics):
    average_holding_time = SerializerMethodField()
    average_holding_time_per_winning_trade = SerializerMethodField()
    average_holding_time_per_lossing_trade = SerializerMethodField()
    average_holding_time_per_long_position = SerializerMethodField()
    average_holding_time_per_short_position = SerializerMethodField()

    class Meta:
        fields = [
            "average_holding_time",
            "average_holding_time_per_winning_trade",
            "average_holding_time_per_lossing_trade",
            "average_holding_time_per_long_position",
            "average_holding_time_per_short_position",
        ]


class PositionVolumeSerializer(MetricsSerializerMixin, GetPositionVolume):
    # Min Position volume
    min_position_volume = SerializerMethodField()
    min_position_volume_per_winning_trade = SerializerMethodField()
    min_position_volume_per_losing_trade = SerializerMethodField()

    # Max Position volume
    max_position_volume = SerializerMethodField()
    max_position_volume_per_winning_trade = SerializerMethodField()
    max_position_volume_per_losing_trade = SerializerMethodField()

    # Average Position volume
    average_position_volume = SerializerMethodField()
    average_position_volume_per_long_position = SerializerMethodField()
    average_position_volume_per_short_position = SerializerMethodField()
    average_position_volume_per_winning_trade = SerializerMethodField()
    average_position_volume_per_losing_trade = SerializerMethodField()

    class Meta:
        fields = [
            "min_position_volume",
            "min_position_volume_per_winning_trade",
            "min_position_volume_per_losing_trade",
            "max_position_volume",
            "max_position_volume_per_winning_trade",
            "max_position_volume_per_losing_trade",
            "average_position_volume",
            "average_position_volume_per_winning_trade",
            "average_position_volume_per_losing_trade",
            "average_position_volume_per_long_position",
            "average_position_volume_per_short_position",
        ]
