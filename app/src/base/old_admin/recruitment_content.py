from typing import ClassVar

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from base.admin.base import BaseAdmin
from base.models import RecruitmentArticle


@admin.register(RecruitmentArticle)
class RecruitmentArticleAdmin(SimpleHistoryAdmin, BaseAdmin):
    """
    (管理画面) 採用記事
    """

    actions = None

    list_display: ClassVar = [
        'company',
        'name',
        'media',
    ]

    list_filter: ClassVar = [
        'company',
    ]

    list_display_links: ClassVar = [
        'name',
    ]

    readonly_fields: ClassVar = [
        'company',
        'name',
        'url',
        'media',
    ]

    exclude: ClassVar = [
        'deleted_at',
    ]

