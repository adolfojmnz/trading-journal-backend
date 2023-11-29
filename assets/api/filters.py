from django_filters import rest_framework as filters

from assets.models import CurrencyPair


class CurrencyPairFilterBackend(filters.DjangoFilterBackend):
    def get_filterset_kwargs(self, request, queryset, view):
        kwargs = super().get_filterset_kwargs(request, queryset, view)

        if hasattr(view, "get_filterset_kwargs"):
            kwargs.update(view.get_filterset_kwargs())

        return kwargs


class CurrencyPairFilterSet(filters.FilterSet):
    symbol = filters.CharFilter(
        "symbol", lookup_expr="icontains",
    )
    base_currency_symbol = filters.CharFilter(
        "base_currency__symbol", lookup_expr="icontains",
    )
    quote_currency_symbol = filters.CharFilter(
        "quote_currency__symbol", lookup_expr="icontains",
    )
    pip_decimal_position_eq = filters.NumberFilter(
        "pip_decimal_position", lookup_expr="exact"
    )

    class Meta:
        model = CurrencyPair
        fields = [
            "symbol",
            "base_currency_symbol",
            "quote_currency_symbol",
            "pip_decimal_position",
        ]
