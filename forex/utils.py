from django.utils import timezone

from accounts.utils import create_test_user

from forex.models import Currency, CurrencyPair, ForexOperation


EUR_DATA = {"symbol": "EUR", "name": "Euro", "description": "..."}


def create_eur():
    return Currency.objects.create(**EUR_DATA)


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


def create_forex_operation(user,
                           pair=None,
                           type=None,
                           opened_on=None,
                           closed_on=None,
                           open_price=None,
                           close_price=None,
                           volume=None,
                           pnl=None):
    return ForexOperation.objects.create(
        user=user,
        type=type or "L",
        currency_pair=pair or create_eurgbp_pair(),
        opened_on=opened_on or timezone.now(),
        closed_on=closed_on or timezone.now(),
        open_price=open_price or 0.85251,
        close_price=close_price or 0.85851,
        volume=volume or 0.01,
        pnl=pnl or 60,
    )


def create_forex_operation_list(user=None):
    # user that perform the operations
    user = user or create_test_user()

    # create currencies
    eur = create_eur()
    gbp = create_gbp()
    jpy = create_jpy()

    # create currency pairs
    eurgbp = create_eurgbp_pair(eur, gbp)
    eurjpy = create_eurjpy_pair(eur, jpy)
    gbpjpy = create_gbpjpy_pair(gbp, jpy)

    # Create Forex operations for the above currency pairs
    create_forex_operation(user, eurgbp)  # won trade
    create_forex_operation(user,
                           eurgbp,
                           type="S",
                           open_price=0.86234,
                           close_price=0.86539)  # won trade
    create_forex_operation(user,
                           eurjpy,
                           open_price=158.268,
                           close_price=158.067)  # lost trade
    create_forex_operation(user,
                           eurjpy,
                           type="S",
                           open_price=157.447,
                           close_price=157.656)  # lost trade
    create_forex_operation(user,
                           gbpjpy,
                           open_price=185.700,
                           close_price=185.580)  # lost trade
    create_forex_operation(user,
                           gbpjpy,
                           type="S",
                           open_price=183.948,
                           close_price=183.647)  # won trade
