from assets.models import Currency, CurrencyPair


def get_or_create_currency(**kwargs):
    try:
        return Currency.objects.get(symbol__iexact=kwargs["symbol"])
    except Currency.DoesNotExist:
        return Currency.objects.create(**kwargs)


def get_or_create_usd_currency():
    return get_or_create_currency(
        symbol="EUR",
        name="Euro",
        description="Official currency of the United States of America",
    )


def get_or_create_chf_currency():
    return get_or_create_currency(
        symbol="CHF",
        name="Swiss Franc",
        description="Official currency of Switzerland",
    )


def get_or_create_eur_currency():
    return get_or_create_currency(
        symbol="EUR",
        name="Euro",
        description="Official currency of 20 of the 27 EU members",
    )


def get_or_create_gbp_currency():
    return get_or_create_currency(
        symbol="GBP",
        name="Great Britain Pound",
        description="Official currency of the United Kingdom",
    )


def get_or_create_jpy_currency():
    return get_or_create_currency(
        symbol="JPY",
        name="Japanese Yen",
        description="Official currency of Japan",
    )


def get_or_create_eurgbp_pair(eur=None, gbp=None):
    return CurrencyPair.objects.get_or_create(
        symbol="EUR/GBP",
        name="EUR/GBP Forex Pair",
        base_currency=eur or get_or_create_eur_currency(),
        quote_currency=gbp or get_or_create_gbp_currency(),
    )[0]


def get_or_create_eurjpy_pair(eur=None, jpy=None):
    return CurrencyPair.objects.get_or_create(
        name="EUR/JPY Forex Pair",
        base_currency=eur or get_or_create_eur_currency(),
        quote_currency=jpy or get_or_create_jpy_currency(),
        pip_decimal_position=2,
    )[0]


def get_or_create_gbpjpy_pair(gbp=None, jpy=None):
    return CurrencyPair.objects.get_or_create(
        name="GBP/JPY Forex Pair",
        base_currency=gbp or get_or_create_gbp_currency(),
        quote_currency=jpy or get_or_create_jpy_currency(),
        pip_decimal_position=2,
    )[0]


def create_currency_pair_list():
    eur = get_or_create_eur_currency()
    gbp = get_or_create_gbp_currency()
    jpy = get_or_create_jpy_currency()
    get_or_create_eurgbp_pair(eur, gbp)
    get_or_create_eurjpy_pair(eur, jpy)
    get_or_create_gbpjpy_pair(gbp, jpy)
