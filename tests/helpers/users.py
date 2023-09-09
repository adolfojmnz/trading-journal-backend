from accounts.models import User

from tests.data.users import (
    simple_user_data,
    staff_user_data,
    superuser_data,
)


def create_user(user_data, is_public=True, is_staff=False, is_superuser=False):
    user = User.objects.create(
        **user_data,
        is_public=is_public,
        is_staff=is_staff,
        is_superuser=is_superuser,
    )
    return user


def create_simple_user():
    return create_user(
        user_data=simple_user_data
    )


def create_staff_user():
    return create_user(
        user_data=staff_user_data,
        is_staff=True,
    )


def create_superuser():
    return create_user(
        user_data=superuser_data,
        is_staff=True,
        is_superuser=True,
    )
