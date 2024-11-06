from typing import ClassVar

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from base.admin.base import BaseAdmin
from base.models import CompanyStrength


class StrengthAdmin(SimpleHistoryAdmin, BaseAdmin):
    """
    (管理画面設定) 強み
    """

    list_display: ClassVar = [
        "company",
        "strength",
    ]

    readonly_fields: ClassVar = [
        "company",
        "strength",
        "description",
    ]

admin.site.register(CompanyStrength, StrengthAdmin)
