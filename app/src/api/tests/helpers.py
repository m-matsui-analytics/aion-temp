from pathlib import Path

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from base.models import Company
from users.models import CustomUser as User

def create_normal_user() -> User:
    """
    テスト用の一般ユーザーを作成するヘルパー関数
    """
    company = Company.objects.create(name="Test Company")
    return User.objects.create_user(
        email="normaluser@test.com",
        password="testpass123",  # noqa: S106
        company=company,
    )

def create_builder_user() -> User:
    """
    テスト用の`builder`グループユーザーを作成するヘルパー関数
    """
    company = Company.objects.create(name="Test Company")
    user = User.objects.create_user(
        email="builderuser@test.com",
        password="testpass123",  # noqa: S106
        company=company,
    )
    user.groups.create(name="builder")

    return user
