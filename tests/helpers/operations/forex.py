from django.utils import timezone

from tests.helpers.assets.forex.pair import (
    create_eur_gbp_pair,
    create_eur_jpy_pair,
)
from tests.helpers.accounts.trading import create_trading_account

from operations.models import ForexOperation


def create_forex_operation(trading_account,
                           currency_pair,
                           status="OP",
                           volume=0.02,
                           position="LN",
                           open_price="1.07098",
                           close_price="1.07898"):
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


def create_eur_gbp_operation(profit=True):
    return create_forex_operation(
        trading_account=create_trading_account(),
        currency_pair=create_eur_gbp_pair(),
        position="LN" if profit else "SH",
    )