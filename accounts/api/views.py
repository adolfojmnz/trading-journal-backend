from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    SAFE_METHODS,
)
from rest_framework.response import Response
from rest_framework import status

from accounts.models import User, TradingAccount, Transaction
from accounts.api.serializers import (
    UserSerializer,
    TradingAccountSerializer,
    TransactionSerializer,
)


class UserViewMixin:
    model = User
    queryset = model.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.queryset.filter(is_active=True)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def handle_post_request(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def handle_put_request(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def handle_patch_request(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    def handle_request_on_valid_password(self,
                                     handler_func,
                                     request,
                                    *args,
                                    **kwargs):
        password = request.data.get('password')
        try:
            validate_password(password)
            return handler_func(request, *args, **kwargs)
        except ValidationError as error:
            return Response(
                {'Validation Error': f'{error}'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except TypeError as error:
            if request.method in ['PATCH']:
                return handler_func(request, *args, **kwargs)
            return Response(
                {'password': ['This field is required.']},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserListView(UserViewMixin, ListCreateAPIView):

    def post(self, request, *args, **kwargs):
        return self.handle_request_on_valid_password(
            self.handle_post_request,
            request,
            *args,
            **kwargs,
        )


class UserDetailView(UserViewMixin, RetrieveUpdateDestroyAPIView):

    def get_permissions(self):
        if self.request.user == User.objects.get(pk=self.kwargs['pk']):
            self.permission_classes = [IsAuthenticated]
        elif not self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def put(self, request, *args, **kwargs):
        return self.handle_request_on_valid_password(
            self.handle_put_request,
            request,
            *args,
            **kwargs,
        )

    def patch(self, request, *args, **kwargs):
        return self.handle_request_on_valid_password(
            self.handle_patch_request,
            request,
            *args,
            **kwargs,
        )

    def delete(self):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response(
            {'message': 'The user has been set as inactive.'},
            status=status.HTTP_200_OK,
        )


class CurrentUserView(UserDetailView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class TradingAccountListView(ListCreateAPIView):
    model = TradingAccount
    queryset = model.objects.all()
    serializer_class = TradingAccountSerializer


class TradingAccountDetailView(RetrieveUpdateDestroyAPIView):
    model = TradingAccount
    queryset = model.objects.all()
    serializer_class = TradingAccountSerializer


class TransactionListView(ListCreateAPIView):
    model = Transaction
    queryset = model.objects.all()
    serializer_class = TransactionSerializer

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

    def post(self, request, *args, **kwargs):
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
