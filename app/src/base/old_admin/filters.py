"""管理画面のフィルタリング機能を提供するモジュール"""

from typing import TYPE_CHECKING, Any

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from base.models import Company

if TYPE_CHECKING:
    from django.http import HttpRequest, Optional, QuerySet

class ActiveCompanyFilter(admin.SimpleListFilter):
    """
    Companyモデル内で、削除されていない企業のみをフィルタリングする
    """

    title = _('企業')
    parameter_name = 'company'

    def lookups(self, request: 'HttpRequest', model_admin: any) -> list[tuple[Any, str]]:  # noqa: ARG002, E501
        """
        フィルタメニューに表示する選択肢を定義
        """
        companies = Company.objects.filter(deleted_at=None)  # 削除されていない会社のみ取得
        return [(company.id, company.name) for company in companies]

    def queryset(self, request: 'HttpRequest', queryset: 'QuerySet') -> 'Optional[QuerySet]':  # noqa:  ARG002
        """
        選択されたフィルタオプションに応じたクエリセットを返す
        """
        if self.value():
            return queryset.filter(company__id=self.value())
        return queryset
