from django.db import models
from django.contrib.auth.models import AbstractUser


ACCOUNT_TYPE = [
    ("DM", "demo"),
    ("RL", "real"),
]

TRANSACTIONS = [
    ("DP", "deposit"),
    ("WT", "withdrawal"),
]


class User(AbstractUser):
    """
    default fields:
        username, first_name, last_name, email, password, group, user_permissions,
        is_staff, is_active, is_superuser, last_login, date_joined

    for further information refer to https://docs.djangoproject.com/en/4.2/ref/contrib/auth/
    """
    public = models.BooleanField(
        default=True,
        help_text="If True, the profile will be retriverable by other users",
    )

    def __str__(self):
        return self.username


class TradingAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    broker = models.CharField(
        max_length=128,
        help_text="Broker in which the account is registered",
    )
    type = models.CharField(
        default="DM",
        choices=ACCOUNT_TYPE,
        max_length=2,
        help_text="Trading accounts can be either DEMO or REAL",
    )
    equity = models.FloatField(
        default=0.0,
        help_text="Total equity of the trading account",
    )
    total_deposited = models.FloatField(
        default=0.0,
        help_text="Total amount of USD deposited into the trading account",
    )
    total_withdrawn = models.FloatField(
        default=0.0,
        help_text="Total amount of USD withdrawn from the trading account",
    )
    total_lost = models.FloatField(
        default=0.0,
        help_text="Total amount of USD lost on trades"
    )
    total_profited = models.FloatField(
        default=0.0,
        help_text="Total amount of USD profited on trades"
    )
    added_on = models.DateTimeField(
        auto_now_add=True,
        help_text="Datetime at which the account was added to this platform"
    )

    def __str__(self) -> str:
        return f"{self.user}'s account on {self.broker}: {self.equity} USD"


class Transaction(models.Model):
    trading_account = models.ForeignKey(
        TradingAccount, on_delete=models.PROTECT
    )
    type = models.CharField(choices=TRANSACTIONS, max_length=2)
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    concept = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.type} for {self.amount} USD on {self.date} at {self.time}"
