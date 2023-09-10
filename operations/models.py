from django.db import models

from assets.models import CurrencyPair
from accounts.models import TradingAccount


OPERATION_STATUS_CHOICE = [
    ("OP", "open"),
    ("LO", "loss"),
    ("PR", "profit"),
]

OPERATION_POSITION_CHOICE = [
    ("LN", "long"),
    ("SH", "short"),
]


class ForexOperation(models.Model):
    trading_account = models.ForeignKey(TradingAccount, on_delete=models.PROTECT)
    currency_pair = models.ForeignKey(CurrencyPair, on_delete=models.PROTECT)
    status = models.CharField(choices=OPERATION_STATUS_CHOICE, max_length=2)
    open_datetime = models.DateTimeField()
    close_datetime = models.DateTimeField(default=None, blank=True, null=True)
    open_price = models.FloatField()
    close_price = models.FloatField(default=None, blank=True, null=True)
    volume = models.FloatField(default=0.01)
    position = models.CharField(choices=OPERATION_POSITION_CHOICE, max_length=2)
    pips = models.FloatField(default=0.0, help_text="Profit/loss in pips")
    profit = models.FloatField(
        default=0.0,
        help_text="In USD Profit/loss of the operation after closed",
    )

    def save(self):
        if not self.close_price:
            return super().save()
        if self.position == "LN":
            self.pips = self.close_price - self.open_price
        else:
            self.pips = self.open_price - self.close_price

        self.pips *= self.currency_pair.multiplier
        self.profit = self.pips * self.volume * self.currency_pair.usd_per_lot
        return super().save()

    def __str__(self) -> str:
        return f"""
            {self.position} position on
            {self.currency_pair}:
            {self.pips:.2f} PIPs |
            {self.profit:.2f} USD
        """
