from django.contrib import admin

from assets.models import Currency, CurrencyPair


admin.site.register(Currency)
admin.site.register(CurrencyPair)