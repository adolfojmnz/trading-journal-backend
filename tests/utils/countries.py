from tests.utils.assets import (
    get_or_create_eur_currency,
    get_or_create_usd_currency,
    get_or_create_chf_currency,
    get_or_create_gbp_currency,
    get_or_create_jpy_currency,
)

from countries.models import Country


def get_or_create_country(**kwargs):
    try:
        country = Country.objects.get(code__iexact=kwargs["code"])
    except Country.DoesNotExist:
        country = Country.objects.create(**kwargs)
    return country


def get_or_create_ge_country():
    return get_or_create_country(
        name="Germany",
        code="GE",
        currency=get_or_create_eur_currency(),
    )


def get_or_create_us_country():
    return get_or_create_country(
        name="United States of America",
        code="US",
        currency=get_or_create_usd_currency(),
    )


def get_or_create_ch_country():
    return get_or_create_country(
        name="Switzerland",
        code="CH",
        currency=get_or_create_chf_currency(),
    )


def get_or_create_uk_country():
    return get_or_create_country(
        name="United Kingdom",
        code="UK",
        currency=get_or_create_gbp_currency(),
    )


def get_or_create_jp_country():
    return get_or_create_country(
        name="Japan",
        code="JP",
        currency=get_or_create_jpy_currency(),
    )


def get_or_create_country_list():
    results = []
    results.append(get_or_create_ge_country())
    results.append(get_or_create_us_country())
    results.append(get_or_create_ch_country())
    results.append(get_or_create_uk_country())
    results.append(get_or_create_jp_country())
    return results
