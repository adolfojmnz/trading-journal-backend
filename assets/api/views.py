from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import (
    SAFE_METHODS,
    IsAdminUser,
    IsAuthenticated,
)

from assets.models import Currency, CurrencyPair
from assets.api.serializers import (
    CurrencySerializer,
    CurrencyPairSerializer,
)


class PermissionsMixin:
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method not in SAFE_METHODS:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class CurrencyListView(PermissionsMixin, ListCreateAPIView):
    model = Currency
    queryset = model.objects.all()
    serializer_class = CurrencySerializer


class CurrencyDetailView(PermissionsMixin, RetrieveUpdateDestroyAPIView):
    model = Currency
    queryset = model.objects.all()
    serializer_class = CurrencySerializer


class CurrencyPairListView(PermissionsMixin, ListCreateAPIView):
    model = CurrencyPair
    queryset = model.objects.all()
    serializer_class = CurrencyPairSerializer


class CurrencyPairDetailView(PermissionsMixin, RetrieveUpdateDestroyAPIView):
    model = CurrencyPair
    queryset = model.objects.all()
    serializer_class = CurrencyPairSerializer
