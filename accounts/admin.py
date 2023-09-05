from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import User, TradingAccount, Transaction


class CustomUserAdmin(UserAdmin):
    model = User


admin.site.register(User)
admin.site.register(TradingAccount)
admin.site.register(Transaction)
