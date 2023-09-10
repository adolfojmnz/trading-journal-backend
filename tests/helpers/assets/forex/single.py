from assets.models import Currency

from tests.data.assets.forex import single


def create_currency(currency_data):
    return Currency.objects.create(**currency_data)


def create_eur_currency():
    return create_currency(single.eur)


def create_gbp_currency():
    return create_currency(single.gbp)


def create_jpy_currency():
    return create_currency(single.jpy)