
from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class IsBuilderUser(BasePermission):
    """
    ビルダーユーザーのみアクセス可能なパーミッションクラス
    """

    def has_permission(self, request: Request, view) -> bool:  # noqa: D102
        return request.user.groups.filter(name="builder").exists()
