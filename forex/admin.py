from django.contrib import admin

from forex.models import Currency, CurrencyPair, ForexOperation


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


@admin.register(ForexOperation)
class ForexOperationAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "ticket",
        "type",
        "open_datetime",
        "close_datetime",
        "stop_loss",
        "take_profit",
        "volume",
        "pnl"
    ]