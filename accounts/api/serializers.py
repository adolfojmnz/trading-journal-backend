from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from accounts.models import User, TradingAccount, Transaction


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_active',
            'is_staff',
            'is_superuser',
            'last_login',
            'date_joined',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'read_only': True},
            'is_staff': {'read_only': True},
        }

    def save(self, **kwargs):
        try:
            self.validated_data['password'] = make_password(
                self.validated_data['password']
            )
        except KeyError:
            pass
        finally:
            return super().save(**kwargs)


class TradingAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = TradingAccount
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'
