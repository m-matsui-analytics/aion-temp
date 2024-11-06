from typing import Any, ClassVar

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
    TokenVerifySerializer,
)

from users.models import CustomUser as User


class UserSerializer(serializers.ModelSerializer):
    """
    ユーザーシリアライザ
    """

    company_name = serializers.CharField(source="company.name", read_only=True)

    class Meta:  # noqa: D106
        model = User
        fields: ClassVar = [
            'company_name',
            'account_status',
        ]

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    djangorestframework-simplejwtのTokenObtainPairSerializerをカスタム

    ユーザーIDをトークンのペイロードに追加
    """

    def validate(self, attrs):
        # 既存のバリデーションを行い、トークンを生成
        data = super().validate(attrs)

        # ユーザーIDをトークンのペイロードに追加
        data['user_id'] = self.user.id

        return data

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """
    djangorestframework-simplejwtのTokenRefreshSerializerをカスタム
    """

    # def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:  # noqa: D102
    #     # デフォルトの検証を実行
    #     data = super().validate(attrs)

    #     # `is_api_user`がTrueかどうか確認
    #     if not self.user.is_api_user:
    #         raise AuthenticationFailed(_(''), code='authorization')

    #     return data

class CustomTokenVerifySerializer(TokenVerifySerializer):
    """
    djangorestframework-simplejwtのTokenVerifySerializerをカスタム
    """

    # def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:  # noqa: D102
    #     # デフォルトの検証を実行
    #     data = super().validate(attrs)

    #     # `is_api_user`がTrueかどうか確認
    #     if not self.user.is_api_user:
    #         raise AuthenticationFailed(_(''), code='authorization')

    #     return data
