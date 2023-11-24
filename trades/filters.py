from django_filters import rest_framework as filters

from trades.models import Trade


class TradeFilterBackend(filters.DjangoFilterBackend):
    def get_filterset_kwargs(self, request, queryset, view):
        kwargs = super().get_filterset_kwargs(request, queryset, view)

        if hasattr(view, "get_filterset_kwargs"):
            kwargs.update(view.get_filterset_kwargs())

        return kwargs


class TradeFilterSet(filters.FilterSet):
    """ Filter set for the Trade model.

        This filter set provides a set of filters for querying Trade
        objects based on various fields such as asset, ticket, type,
        open date, close date, volume, pnl (profit and loss), and more.
    """
    asset = filters.CharFilter(
        "currency_pair__symbol", lookup_expr="icontains",
    )
    ticket = filters.NumberFilter(
        "ticket", lookup_expr="contains",
    )
    type = filters.CharFilter(
        "type", lookup_expr="iexact",
    )
    open_date_eq = filters.DateFilter(
        "open_datetime", lookup_expr="date__exact",
    )
    open_date_gte = filters.DateFilter(
        "open_datetime", lookup_expr="date__gte",
    )
    open_date_lte = filters.DateFilter(
        "open_datetime", lookup_expr="date__lte",
    )
    close_date_eq = filters.DateFilter(
        "close_datetime", lookup_expr="date__exact",
    )
    close_date_gte = filters.DateFilter(
        "close_datetime", lookup_expr="date__gte",
    )
    close_date_lte = filters.DateFilter(
        "close_datetime", lookup_expr="date__lte",
    )
    volume_eq = filters.NumberFilter(
        "volume", lookup_expr="exact",
    )
    volume_gte = filters.NumberFilter(
        "volume", lookup_expr="gte",
    )
    volume_lte = filters.NumberFilter(
        "volume", lookup_expr="lte",
    )
    pnl_eq = filters.NumberFilter(
        "pnl", lookup_expr="exact",
    )
    pnl_gte = filters.NumberFilter(
        "pnl", lookup_expr="gte",
    )
    pnl_lte = filters.NumberFilter(
        "pnl", lookup_expr="lte",
    )
    profit_eq = filters.NumberFilter(
        "pnl",
        lookup_expr="exact",
        method="profit_eq_filter",
        label="profit is equal to",
    )
    profit_gte = filters.NumberFilter(
        "pnl",
        lookup_expr="gte",
        method="profit_gte_filter",
        label="profit is greater than or equal to",
    )
    profit_lte = filters.NumberFilter(
        "pnl",
        lookup_expr="lte",
        method="profit_lte_filter",
        label="profit is less than or equal to",
    )
    loss_eq = filters.NumberFilter(
        "pnl",
        lookup_expr="exact",
        method="loss_eq_filter",
        label="loss is equal to",
    )
    loss_gte = filters.NumberFilter(
        "pnl",
        lookup_expr="gte",
        method="loss_gte_filter",
        label="loss is greater than or equal to",
    )
    loss_lte = filters.NumberFilter(
        "pnl",
        lookup_expr="lte",
        method="loss_lte_filter",
        label="loss is less than or equal to",
    )

    def profit_eq_filter(self, queryset, name, value):
        """ Filters trades with a profit magnitude
            equal to the specified value.
        """
        return queryset.filter(pnl__gt=0).filter(pnl__exact=value)

    def profit_gte_filter(self, queryset, name, value):
        """ Filters trades with a profit magnitude
            greater than or equal to the specified value.
        """
        return queryset.filter(pnl__gt=0).filter(pnl__gte=value)

    def profit_lte_filter(self, queryset, name, value):
        """ Filters trades with a profit magnitude
            less than or equal to the specified value.
        """
        return queryset.filter(pnl__gt=0).filter(pnl__lte=value)

    def loss_eq_filter(self, queryset, name, value):
        """ Filters trades with a loss magnitude
            equal to the specified value.
        """
        value = -abs(value)
        return queryset.filter(pnl__lt=0).filter(pnl__exact=value)

    def loss_gte_filter(self, queryset, name, value):
        """ Filters trades with a loss magnitude greater
            than or equal to the specified value.
        """
        value = -abs(value)
        return queryset.filter(pnl__lt=0).filter(pnl__lte=value)

    def loss_lte_filter(self, queryset, name, value):
        """ Filters trades with a loss magnitude less than or equal
            to the specified value.
        """
        value = -abs(value)
        return queryset.filter(pnl__lt=0).filter(pnl__gte=value)

    class Meta:
        model = Trade
        fields = [
            "asset",
            "ticket",
            "type",
            "open_date_eq",
            "open_date_gte",
            "open_date_lte",
            "close_date_eq",
            "close_date_gte",
            "close_date_lte",
            "volume_eq",
            "volume_gte",
            "volume_lte",
            "pnl_eq",
            "pnl_gte",
            "pnl_lte",
            "profit_eq",
            "profit_gte",
            "profit_lte",
            "loss_eq",
            "loss_gte",
            "loss_lte",
        ]
