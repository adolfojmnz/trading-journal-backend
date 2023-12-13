from countries.models import EconomicIndicator

from tests.utils.countries import (
    get_or_create_us_country,
    get_or_create_uk_country,
    get_or_create_ch_country,
)


def get_or_create_economic_indicator(data):
    try:
        return EconomicIndicator.objects.get(
            name=data["name"],
            country__code=data["country"].pk,
        )
    except EconomicIndicator.DoesNotExist:
        return EconomicIndicator.objects.create(**data)


def get_or_create_us_economic_indicator():
    data = {
        "country": get_or_create_us_country(),
        "name": "ADP Employment Change(Nov)",
        "description": "...",
    }
    return get_or_create_economic_indicator(data)


def get_or_create_uk_economic_indicator():
    data = {
        "country": get_or_create_uk_country(),
        "name": "Financial Stability",
        "description": "...",
    }
    return get_or_create_economic_indicator(data)


def get_or_create_ch_economic_indicator():
    data = {
        "country": get_or_create_ch_country(),
        "name": "Foreign Bond Investment",
        "description": "...",
    }
    return get_or_create_economic_indicator(data)


def get_or_create_economic_indicator_list():
    return [
        get_or_create_us_economic_indicator(),
        get_or_create_uk_economic_indicator(),
        get_or_create_ch_economic_indicator(),
    ]
