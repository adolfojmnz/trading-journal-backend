from django.contrib.auth.hashers import make_password

from accounts.models import User


def get_or_create_test_user() -> User:
    return User.objects.get_or_create(
        username="test-user",
        first_name="Testname",
        last_name="Testlastname",
        email="test-email@tester.com",
        password=make_password("test#pass"),
    )[0]


def get_or_create_test_admin() -> User:
    return User.objects.get_or_create(
        is_staff=True,
        username="test-admin",
        first_name="testname",
        last_name="testlastname",
        email="admin-test@localhost.com",
        password=make_password("admin#tess-pw"),
    )[0]

