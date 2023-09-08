from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from accounts.models import TradingAccount, Transaction
from accounts.api.serializers import TradingAccountSerializer


class GetQuerysetMixin:
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(
            user=self.request.user
        )


class TradingAccountListView(GetQuerysetMixin, ListCreateAPIView):
    model = TradingAccount
    queryset = model.objects.all()
    serializer_class = TradingAccountSerializer

    def make_initial_deposit(self, serializer):
        """ Make a deposit transaction with the provided equity """
        trading_account = serializer.instance
        deposit_amount = serializer.validated_data["equity"]
        transaction = Transaction.objects.create(
            trading_account=trading_account,
            type="DP",
            amount=deposit_amount,
            concept="Initial Deposit",
        )
        trading_account.equity = deposit_amount
        trading_account.total_deposited += deposit_amount
        transaction.save()
        trading_account.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        if serializer.validated_data["equity"]:
            self.make_initial_deposit(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class TradingAccountDetailView(GetQuerysetMixin, RetrieveUpdateDestroyAPIView):
    model = TradingAccount
    queryset = model.objects.all()
    serializer_class = TradingAccountSerializer