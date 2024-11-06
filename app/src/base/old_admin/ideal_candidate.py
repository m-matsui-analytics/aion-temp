from typing import TYPE_CHECKING, ClassVar

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from base.admin.base import BaseAdmin
from base.models import IdealCandidate, IdealCandidateRequirement

if TYPE_CHECKING:
    from django.http import HttpRequest

class IdealCandidateRequirementInline(admin.TabularInline):
    """
    (管理画面) 求める人物像の条件
    """

    model = IdealCandidateRequirement



    ordering: ClassVar = ['requirement_level']

    def has_add_permission(self, request: 'HttpRequest', obj: IdealCandidateRequirement | None=None) -> bool:  # noqa: ARG002, D102, E501
        return False

    def has_change_permission(self, request: 'HttpRequest', obj: IdealCandidateRequirement | None=None) -> bool:  # noqa: ARG002, D102, E501
        return False

    def has_delete_permission(self, request: 'HttpRequest', obj: IdealCandidateRequirement | None=None) -> bool:  # noqa: ARG002, D102, E501
        return False

class IdealCandidateAdmin(SimpleHistoryAdmin, BaseAdmin):
    """
    (管理画面) 求める人物像

    Inlines:
        - IdealCandidateRequirementInline
    """

    inlines: ClassVar = [
        IdealCandidateRequirementInline
    ]

    readonly_fields: ClassVar = [
        'company',
        'name',
        'age_min',
        'age_max',
        'work_value_1',
        'work_value_2',
        'work_value_3',
    ]

    exclude: ClassVar = ['deleted_at']

admin.site.register(IdealCandidate, IdealCandidateAdmin)
