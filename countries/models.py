from django.db import models

from assets.models import Currency


class Country(models.Model):
    name = models.CharField(
        unique=True,
        max_length=64,
    )
    code = models.CharField(
        unique=True,
        max_length=2,
        db_index=True,
        help_text="ISO 3166 code",
    )
    currency = models.ForeignKey(
        Currency,
        related_name="country",
        on_delete=models.PROTECT,
    )

    def save(self, *args, **kwargs):
        self.code = self.code.lower()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code.upper()} - {self.name}"


class EconomicIndicator(models.Model):
    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        related_name="economic_indicators",
    )
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ["country", "name"]


class EconomicReport(models.Model):
    class ImpactLevel(models.IntegerChoices):
        low = 1
        mid = 2
        high = 3

    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    impact_level = models.IntegerField(choices=ImpactLevel.choices)
    datetime = models.DateTimeField(
        help_text="Publication datetime of the economic report"
    )
    economic_indicator = models.ForeignKey(
        EconomicIndicator,
        on_delete=models.PROTECT,
        related_name="economic_reports",
    )
    unit = models.CharField(default="", max_length=8)
    actual = models.FloatField(blank=True, null=True)
    forecast = models.FloatField(blank=True, null=True)
    previous = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ["economic_indicator", "datetime"]
