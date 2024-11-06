from collections.abc import Sequence
from typing import TYPE_CHECKING

from django.contrib import admin
from django.utils import timezone

if TYPE_CHECKING:
    from django.http import HttpRequest, Model, QuerySet

class BaseAdmin(admin.ModelAdmin):
    """
    (管理画面設定) 基底クラス
    """

    # def get_queryset(self, request: ("HttpRequest")) -> ("QuerySet"):
    #     """
    #     論理削除されたデータ（deleted_atがNoneではないデータ）を除外
    #     """  # noqa: RUF002
    #     qs = super().get_queryset(request)
    #     return qs.filter(deleted_at=None)


    def delete_model(self, request: "HttpRequest", obj: "Model") -> None:  # noqa: ARG002
        """
        Modelのdelete()を呼び出す
        """
        obj.delete()


    def delete_queryset(self, request: "HttpRequest", queryset: "QuerySet") -> None:  # noqa: ARG002
        """
        一括削除時に論理削除を行う
        """
        queryset.update(deleted_at=timezone.now())  # 論理削除

