from assets.models import CurrencyPair

from tests.data.assets.forex import pair
from tests.helpers.assets.forex import single


def create_currency_pair(pair_data, base_currency, quote_currency):
    return CurrencyPair.objects.create(
        **pair_data,
        base_currency=base_currency,
        quote_currency=quote_currency,
    )


def create_eur_gbp_pair():
    return create_currency_pair(
        pair.eur_gbp,
        base_currency=single.create_eur_currency(),
        quote_currency=single.create_gbp_currency(),
    )


def create_eur_jpy_pair():
    return create_currency_pair(
        pair.eur_jpy,
        base_currency=single.create_eur_currency(),
        quote_currency=single.create_jpy_currency(),
    )


def create_gbp_jpy_pair():
    return create_currency_pair(
        pair.gbp_jpy,
        base_currency=single.create_gbp_currency(),
        quote_currency=single.create_jpy_currency(),
    )