from django.db import models

from accounts.models import User

from assets.models import CurrencyPair


OPERATION_TYPE_CHOICE = [
    ("L", "Long"),
    ("S", "Short")
]


class Trade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.IntegerField(
        unique=True,
        db_index=True,
        help_text="ID of the trade on the trading platform"
    )
    type = models.CharField(max_length=1, choices=OPERATION_TYPE_CHOICE)
    currency_pair = models.ForeignKey(CurrencyPair, on_delete=models.PROTECT)
    open_datetime = models.DateTimeField()
    close_datetime = models.DateTimeField()
    open_price = models.FloatField()
    stop_loss = models.FloatField()
    take_profit = models.FloatField()
    close_price = models.FloatField()
    volume = models.FloatField(default=0.01)
    pnl = models.FloatField(help_text="Profit/loss in USD")

    def __str__(self) -> str:
        return f"{self.type} on {self.currency_pair.symbol}"