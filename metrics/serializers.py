from django.db.models import Sum, Max, Min, Avg

from rest_framework.serializers import Serializer
from rest_framework.serializers import SerializerMethodField

from forex.models import ForexOperation


class ForexMetricsSerializer(Serializer):

    def __init__(self, request, *args, **kwargs):
        self.queryset = ForexOperation.objects.filter(user=request.user)
        return super().__init__(*args, **kwargs)

    def get_total_net_profit(self, *args, **kwargs):
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

    total_net_profit = SerializerMethodField()
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

    class Meta:
        fields = [
            "total_net_profit",
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
        ]