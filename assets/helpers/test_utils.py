from assets.models import Currency, CurrencyPair

EUR_DATA = {"symbol": "EUR", "name": "Euro", "description": "..."}


def create_eur():
    return Currency.objects.create(
        symbol="EUR",
        name="Euro",
        description="Official currency of 20 of the 27 EU nations",
    )


def create_gbp():
    return Currency.objects.create(
        symbol="GBP",
        name="Great Britain Pound",
        description="Official currency of the United Kingdom",
    )


def create_jpy():
    return Currency.objects.create(
        symbol="JPY",
        name="Japanese Yen",
        description="Official currency of Japan",
    )


def create_eurgbp_pair(eur=None, gbp=None):
    return CurrencyPair.objects.create(
        symbol="EUR/GBP",
        name="EUR/GBP Forex Pair",
        base_currency=eur or create_eur(),
        quote_currency=gbp or create_gbp(),
    )


def create_eurjpy_pair(eur=None, jpy=None):
    return CurrencyPair.objects.create(
        name="EUR/JPY Forex Pair",
        base_currency=eur or create_eur(),
        quote_currency=jpy or create_jpy(),
        pip_decimal_position=2,
    )


def create_gbpjpy_pair(gbp=None, jpy=None):
    return CurrencyPair.objects.create(
        name="GBP/JPY Forex Pair",
        base_currency=gbp or create_gbp(),
        quote_currency=jpy or create_jpy(),
        pip_decimal_position=2,
    )


def create_currency_pair_list():
    eur = create_eur()
    gbp = create_gbp()
    jpy = create_jpy()
    create_eurgbp_pair(eur, gbp)
    create_eurjpy_pair(eur, jpy)
    create_gbpjpy_pair(gbp, jpy)