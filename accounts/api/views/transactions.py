from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from accounts.models import Transaction
from accounts.api.serializers import TransactionSerializer


class TransactionListView(ListCreateAPIView):
    model = Transaction
    queryset = model.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(
            trading_account__user=self.request.user
        )

    def make_deposit(self, trading_account, amount):
        trading_account.equity += amount
        trading_account.total_deposited += amount
        trading_account.save()

    def make_withdrawal(self, trading_account, amount):
        trading_account.equity -= amount
        trading_account.total_withdrawn += amount
        trading_account.save()

    def make_transaction(self, serializer):
        trading_account = serializer.validated_data["trading_account"]
        transaction_type = serializer.validated_data["type"]
        transaction_amount = serializer.validated_data["amount"]
        if transaction_type == "WT":
            return self.make_withdrawal(trading_account, transaction_amount)
        return self.make_deposit(trading_account, transaction_amount)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.make_transaction(serializer)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class TransactionDetailView(RetrieveUpdateDestroyAPIView):
    model = Transaction
    queryset = model.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(
            trading_account__user=self.request.user
        )