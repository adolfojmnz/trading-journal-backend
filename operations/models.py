from django.db import models

from currency.models import CurrencyPair


OPERATION_STATUS = [
    ("OP", "open"),
    ("LO", "loss"),
    ("PR", "profit"),
]

POSITIONS = [
    ("LN", "long"),
    ("SH", "short"),
]

class Operation(models.Model):
    currency_pair = models.ForeignKey(
        CurrencyPair,
        on_delete=models.PROTECT,
    )
    status = models.CharField(choices=OPERATION_STATUS, max_length=2)
    open_datetime = models.DateTimeField()
    close_datetime = models.DateTimeField(default=None, blank=True, null=True)
    open_price = models.FloatField()
    close_price = models.FloatField(default=None, blank=True, null=True)
    volume = models.FloatField(default=0.01)
    leverage = models.IntegerField(default=100)
    position = models.CharField(
        choices=POSITIONS,
        max_length=2,
        help_text="Operation type, e.g long for buy",
    )
    pips = models.FloatField(
        default=0.0,
        help_text="Profit/loss in pips",
    )
    profit = models.FloatField(
        default=0.0,
        help_text="In USD Profit/loss of the operation after closed"
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