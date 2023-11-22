from django.db import models

from accounts.models import User


class Currency(models.Model):
    symbol = models.CharField(
        unique=True,
        max_length=3,
        help_text="ISO 4217 Currency Code",
    )
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.symbol


class CurrencyPair(models.Model):
    symbol = models.CharField(
        null=True,
        blank=True,
        unique=True,
        max_length=64,
    )
    name = models.CharField(
        blank=True,
        null=True,
        default=None,
        max_length=128,
    )
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
    pip_decimal_position = models.IntegerField(
        default=4, help_text="Decimal position use to calculate pip movement."
    )

    def save(self, *args, **kwargs):
        if not self.symbol:
            self.symbol = f"{self.base_currency}/{self.quote_currency}"
        if not self.name:
            self.name = f"{self.symbol} ForexPair"
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.symbol
