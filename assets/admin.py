from django.contrib import admin

from assets.models import Currency, CurrencyPair


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ["symbol", "name", "description"]


@admin.register(CurrencyPair)
class CurrencyPairAdmin(admin.ModelAdmin):
    list_display = [
        "symbol",
        "name",
        "base_currency",
        "quote_currency",
        "pip_decimal_position",
    ]
