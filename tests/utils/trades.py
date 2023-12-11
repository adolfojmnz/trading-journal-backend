import time
import random

from django.utils import timezone

from tests.utils.accounts import get_or_create_test_user

from trades.models import Trade

from tests.utils.assets import (
    get_or_create_eur_currency,
    get_or_create_gbp_currency,
    get_or_create_jpy_currency,
    get_or_create_eurgbp_pair,
    get_or_create_eurjpy_pair,
    get_or_create_gbpjpy_pair,
)


def generate_ticket_number():
    """ Generates a big integer ID based on the current
        time and a sequence number. """
    current_time = time.time()
    sequence_number = random.randint(0, 1000)
    return int(current_time) + sequence_number


def create_forex_trade(
    user,
    ticket=None,
    type=None,
    pair=None,
    open_datetime=None,
    close_datetime=None,
    open_price=None,
    close_price=None,
    stop_loss=None,
    take_profit=None,
    volume=None,
    pnl=None,
):
    return Trade.objects.create(
        user=user,
        ticket=ticket or generate_ticket_number(),
        type=type or "L",
        currency_pair=pair or get_or_create_eurgbp_pair(),
        open_datetime=open_datetime or timezone.now(),
        close_datetime=(
            close_datetime or timezone.now() + timezone.timedelta(hours=3)
        ),
        open_price=open_price or 0.85251,
        close_price=close_price or 0.85851,
        stop_loss=stop_loss or 0.85150,
        take_profit=take_profit or 0.85850,
        volume=volume or 0.01,
        pnl=pnl or 60,
    )


def create_forex_trade_list(user=None):
    # user that perform the trades
    user = user if user else get_or_create_test_user()

    # create currencies
    eur = get_or_create_eur_currency()
    gbp = get_or_create_gbp_currency()
    jpy = get_or_create_jpy_currency()

    # create currency pairs
    eurgbp = get_or_create_eurgbp_pair(eur, gbp)
    eurjpy = get_or_create_eurjpy_pair(eur, jpy)
    gbpjpy = get_or_create_gbpjpy_pair(gbp, jpy)

    # Create Forex trades for the above currency pairs
    create_forex_trade(user, pair=eurgbp)  # won trade
    create_forex_trade(
        user,
        pair=eurgbp,
        type="S",
        open_price=0.86234,
        close_price=0.86539,
        close_datetime=timezone.now() + timezone.timedelta(hours=2),
        pnl=30,
    )  # won trade
    create_forex_trade(
        user,
        pair=eurjpy,
        open_price=158.268,
        close_price=158.067,
        close_datetime=timezone.now() + timezone.timedelta(hours=1),
        pnl=-14.7,
    )  # lost trade
    create_forex_trade(
        user,
        pair=eurjpy,
        type="S",
        open_price=157.447,
        close_price=157.656,
        close_datetime=timezone.now() + timezone.timedelta(hours=4),
        pnl=-14.7,
    )  # lost trade
    create_forex_trade(
        user,
        pair=gbpjpy,
        open_price=185.700,
        close_price=185.580,
        close_datetime=timezone.now() + timezone.timedelta(minutes=30),
        pnl=-9.6,
    )  # lost trade
    create_forex_trade(
        user,
        pair=gbpjpy,
        type="S",
        open_price=183.948,
        close_price=183.647,
        close_datetime=timezone.now() + timezone.timedelta(minutes=45),
        pnl=24,
    )  # won trade
