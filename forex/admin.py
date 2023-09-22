from django.contrib import admin

from forex.models import Currency, CurrencyPair

admin.site.register(Currency)
admin.site.register(CurrencyPair)