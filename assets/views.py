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
from assets.serializers import (
    CurrencySerializer,
    CurrencyPairSerializer,
)


class GetPermissionsMixin:
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if not self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class CurrencyListView(GetPermissionsMixin, ListCreateAPIView):
    model = Currency
    queryset = model.objects.all()
    serializer_class = CurrencySerializer


class CurrencyDetailView(GetPermissionsMixin, RetrieveUpdateDestroyAPIView):
    model = Currency
    queryset = model.objects.all()
    serializer_class = CurrencySerializer


class CurrencyPairListView(GetPermissionsMixin, ListCreateAPIView):
    model = CurrencyPair
    queryset = model.objects.all()
    serializer_class = CurrencyPairSerializer


class CurrencyPairDetailView(GetPermissionsMixin, RetrieveUpdateDestroyAPIView):
    model = CurrencyPair
    queryset = model.objects.all()
    serializer_class = CurrencyPairSerializer