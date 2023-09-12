from tests.helpers.users import create_simple_user

from accounts.models import TradingAccount


def create_trading_account():
    TradingAccount.objects.create(
        user = create_simple_user(),
        broker="Demo Broker",
        type="DM",
        equity=50,
    )