from django.contrib import admin

from forex.models import Currency, CurrencyPair, ForexOperation

admin.site.register(Currency)
admin.site.register(CurrencyPair)
admin.site.register(ForexOperation)