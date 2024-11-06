from django.contrib.auth import get_user_model

from users.models import CustomUser as User


def create_superuser(email: str="test_superuser@test.com", password: str="test_password") -> User:  # noqa: ANN001, ARG001, E501, S107
    """
    スーパーユーザーを作成する
    """
    return get_user_model().objects.create_superuser(
        email=email,
        password=password
    )

def create_admin_user(email: str="test_adminuser@test.com", password: str="test_password") -> User:  # noqa: ANN001, ARG001, E501, S107
    """
    adminユーザーを作成する
    """
    return get_user_model().objects.create_user(
        email=email,
        password=password,
        is_staff=True,
        is_superuser=False
    )


def create_user(email: str="test_user@test.com", password: str="test_password") -> User:  # noqa: ANN001, ARG001, E501, S107
    """
    ユーザーを作成する
    """
    return get_user_model().objects.create_user(
        email=email,
        password=password,
        is_staff=False,
        is_superuser=False
    )


def user_login(client, email: str, password: str) -> bool:  # noqa: ANN001
    """
    ユーザーでログインする
    """
    return client.login(email=email, password=password)
