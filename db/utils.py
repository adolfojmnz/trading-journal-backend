from django.utils import timezone

from accounts.models import User, TradingAccount

from assets.models import Currency, CurrencyPair

from operations.models import ForexOperation

from db.data import (
    simple_user as user_data,
    currencies as currencies_data,
    trading_account as trading_account_data,
)


def create_simple_user():
    return User.objects.create(**user_data)


def create_trading_account(user=None):
    return TradingAccount.objects.create(
        **trading_account_data,
        user=user or create_simple_user(),
    )


def create_eur():
    return Currency.objects.create(**currencies_data["eur"])


def create_gbp():
    return Currency.objects.create(**currencies_data["gbp"])


def create_jpy():
    return Currency.objects.create(**currencies_data["jpy"])


def create_eurgbp_pair(eur=None, gbp=None):
    return CurrencyPair.objects.create(
        name="EUR/GBP Forex Pair",
        base_currency=eur or create_eur(),
        quote_currency=gbp or create_gbp(),
    )


def create_forex_operation(trading_account,
                           currency_pair,
                           status="OP",
                           volume=0.02,
                           position="LN",
                           open_price="0.82453",
                           close_price="0.82754"):
    return ForexOperation.objects.create(
        trading_account=trading_account,
        currency_pair=currency_pair,
        status=status,
        volume=volume,
        open_datetime=timezone.datetime.now()-timezone.timedelta(hours=2),
        close_datetime=timezone.datetime.now(),
        open_price=open_price,
        close_price=close_price,
        position=position,
    )


def create_forex_operations(trading_account=None):
    trading_account = trading_account or create_trading_account()

    # Create Currencies
    eur = create_eur()
    gbp = create_gbp()
    jpy = create_jpy()

    # Create Forex Currency Pairs
    eurgbp = CurrencyPair.objects.create(
        name="EUR/GBP Forex Pair",
        base_currency=eur,
        quote_currency=gbp,
    )
    eurjpy = CurrencyPair.objects.create(
        name="EUR/JPY Forex Pair",
        base_currency=eur,
        quote_currency=jpy,
        pip_decimal_position=2,
    )
    gbpjpy = CurrencyPair.objects.create(
        name="GBP/JPY Forex Pair",
        base_currency=gbp,
        quote_currency=jpy,
        pip_decimal_position=2,
    )

    # Create Forex operations for the above currency pairs
    create_forex_operation(trading_account, eurgbp) # won trade
    create_forex_operation(trading_account,
                           eurgbp,
                           position="SH",
                           open_price=0.86234,
                           close_price=0.86539) # won trade
    create_forex_operation(trading_account,
                           eurjpy,
                           open_price=158.268,
                           close_price=158.067) # lost trade
    create_forex_operation(trading_account,
                           eurjpy,
                           position="SH",
                           open_price=157.447,
                           close_price=157.656) # lost trade
    create_forex_operation(trading_account,
                           gbpjpy,
                           open_price=185.700,
                           close_price=185.580) # lost trade
    create_forex_operation(trading_account,
                           gbpjpy,
                           position="SH",
                           open_price=183.948,
                           close_price=183.647) # won trade