from django_filters import rest_framework as filters

from countries.models import Country, EconomicIndicator, EconomicReport


class FilterBackend(filters.DjangoFilterBackend):
    def get_filterset_kwargs(self, request, queryset, view):
        kwargs = super().get_filterset_kwargs(request, queryset, view)

        if hasattr(view, "get_filterset_kwargs"):
            kwargs.update(view.get_filterset_kwargs())

        return kwargs


class ReportFilterSet(filters.FilterSet):
    name = filters.CharFilter(
        "name", lookup_expr="icontains",
    )
    impact = filters.NumberFilter(
        "impact_level", lookup_expr="exact",
    )
    date = filters.DateFilter(
        "datetime", lookup_expr="date__exact",
    )
    country = filters.CharFilter(
        "economic_indicator__country__code", lookup_expr="iexact",
    )
    indicator = filters.NumberFilter(
        "economic_indicator__pk", lookup_expr="exact",
    )

    class Meta:
        model = EconomicReport
        fields = [
            "name",
            "impact",
            "date",
            "country",
            "indicator",
        ]


class IndicatorFilterSet(filters.FilterSet):
    name = filters.CharFilter(
        "name", lookup_expr="icontains",
    )
    country = filters.CharFilter(
        "country__code", lookup_expr="iexact",
    )
    currency = filters.NumberFilter(
        "country__currency__pk", lookup_expr="exact",
    )

    class Meta:
        model = EconomicIndicator
        fields = [
            "name",
            "country",
            "currency",
        ]


class CountryFilterSet(filters.FilterSet):
    name = filters.CharFilter(
        "name", lookup_expr="icontains",
    )
    code = filters.CharFilter(
        "code", lookup_expr="iexact",
    )
    currency = filters.NumberFilter(
        "currency__pk", lookup_expr="exact",
    )

    class Meta:
        model = Country
        fields = [
            "name",
            "code",
            "currency",
        ]
