from typing import ClassVar

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from base.admin.base import BaseAdmin
from base.admin.filters import ActiveCompanyFilter
from base.models import JobPosting


@admin.register(JobPosting)
class JobPostingAdmin(SimpleHistoryAdmin, BaseAdmin):
    """
    (管理画面) 求人情報
    """

    actions = None

    list_display: ClassVar = [
        'company',
        'name',
        'media',
    ]

    list_filter: ClassVar = [
        ActiveCompanyFilter,
        # 'company',
    ]

    list_display_links: ClassVar = [
        'name',
    ]

    # readonly_fields: ClassVar = [
    #     'company',
    #     'name',
    #     'url',
    #     'media',
    #     'search_info',
    # ]

    exclude: ClassVar = [
        'deleted_at',
    ]
