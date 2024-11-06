from typing import TYPE_CHECKING, ClassVar

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from simple_history.admin import SimpleHistoryAdmin

from base.admin.base import BaseAdmin
from base.models import Company, CompanyInfo, CompanyMedia

if TYPE_CHECKING:
    from django.http import HttpRequest

class CompanyInfoInline(admin.StackedInline):
    """
    (管理画面設定) 会社概要モデル
    """

    model = CompanyInfo

    # readonly_fields: ClassVar = [
    #     "foundation_date",
    #     "capital",
    #     "post_code",
    #     "address_prefecture",
    #     "address_other",
    #     "ceo_name",
    #     "employee_size",
    #     "business_description",
    #     "industry",
    #     "revenue",
    #     "mission",
    #     "vision",
    #     "value",
    # ]


    def has_add_permission(self, request: 'HttpRequest', obj: CompanyInfo | None=None) -> bool:  # noqa: ARG002, D102, E501
        return False

    def has_change_permission(self, request: 'HttpRequest', obj: CompanyInfo | None=None) -> bool:  # noqa: ARG002, D102, E501
        return False

    def has_delete_permission(self, request: 'HttpRequest', obj: CompanyInfo | None=None) -> bool:  # noqa: ARG002, D102, E501
        return False

class CompanyMediaInline(admin.StackedInline):
    """
    (管理画面設定) 利用している採用媒体
    """

    model = CompanyMedia

    extra: ClassVar = 0

    def has_add_permission(self, request: 'HttpRequest', obj: CompanyInfo | None=None) -> bool:  # noqa: ARG002, D102, E501
        return False

    def has_change_permission(self, request: 'HttpRequest', obj: CompanyInfo | None=None) -> bool:  # noqa: ARG002, D102, E501
        return False

    def has_delete_permission(self, request: 'HttpRequest', obj: CompanyInfo | None=None) -> bool:  # noqa: ARG002, D102, E501
        return False

class CompanyAdmin(SimpleHistoryAdmin, BaseAdmin):
    """
    (管理画面設定) 企業モデル
    """

    inlines: ClassVar = [
        CompanyInfoInline,
        CompanyMediaInline,
    ]

    list_display: ClassVar = [
        "name",
        "plan",
        "is_tutorial_completed",
    ]

    readonly_fields: ClassVar = [
        "plan",
        "fiscal_year_start_month",
        "is_tutorial_completed",
    ]


admin.site.register(Company, CompanyAdmin)




