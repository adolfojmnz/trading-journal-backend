from django.contrib import admin

from trades.models import Trade


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "ticket",
        "currency_pair",
        "type",
        "open_datetime",
        "close_datetime",
        "stop_loss",
        "take_profit",
        "volume",
        "pnl",
    ]
