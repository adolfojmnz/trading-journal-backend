from django.db import models


class Currency(models.Model):
    symbol = models.CharField(
        max_length=3,
        help_text="ISO 4217 Currency Code",
    )
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.symbol


class CurrencyPair(models.Model):
    symbol = models.CharField(max_length=64, blank=True, null=True)
    description = models.CharField(max_length=128)
    base_currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name="base_currency",
        help_text="Currency that is being bought or sold",
    )
    quote_currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name="quote_currency",
        help_text="Currency that is used to price the base currency",
    )
    usd_per_lot = models.FloatField(
        default=10,
        help_text="Quantity of USD per standard lot",
    )
    pnl_multiplier = models.IntegerField(
        default=10000,
        help_text="Value used to calculate the total profit/loss in pips",
    )
    swap_long = models.FloatField(
        default=0.0,
        help_text="In-points overnight interest for a long position",
    )
    swap_short = models.FloatField(
        default=0.0,
        help_text="In-points overnight interest for a short position",
    )

    def save(self, *args, **kwargs):
        self.symbol = f"{self.base_currency}/{self.quote_currency}"
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.symbol