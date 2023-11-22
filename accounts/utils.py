from django.contrib.auth.hashers import make_password

from accounts.models import User


def create_test_user() -> User:
    return User.objects.create(
        username="test-user",
        first_name="Testname",
        last_name="Testlastname",
        email="test-email@tester.com",
        password=make_password("test#pass"),
    )


def create_test_admin() -> User:
    return User.objects.create(
        is_staff=True,
        username="test-admin",
        first_name="testname",
        last_name="testlastname",
        email="admin-test@localhost.com",
        password=make_password("admin#tess-pw"),
    )
