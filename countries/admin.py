from django.contrib import admin

from countries.models import Country, EconomicReport, EconomicIndicator

admin.site.register(Country)
admin.site.register(EconomicReport)
admin.site.register(EconomicIndicator)
