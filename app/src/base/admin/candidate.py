from typing import ClassVar

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from base.forms import CandidateCreateForm
from base.models import (
    Candidate,
    CandidateAcademicHistory,
    CandidateCertification,
    CandidatePreferredIndustry,
    CandidatePreferredLocation,
    CandidatePreferredOccupation,
    CandidateSkill,
    CandidateWorkHistory,
    Scout,
)


####################################################################
# InlineModel
####################################################################
class CandidatePreferredIndustryInline(admin.TabularInline):
    """
    (管理画面設定) 候補者希望業界
    """

    model = CandidatePreferredIndustry

class CandidatePreferredOccupationInline(admin.TabularInline):
    """
    (管理画面設定) 候補者希望職種
    """

    model = CandidatePreferredOccupation

class CandidatePreferredLocationInline(admin.TabularInline):
    """
    (管理画面設定) 候補者希望勤務地
    """

    model = CandidatePreferredLocation


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    """
    (管理画面設定) 候補者
    """

    inlines: ClassVar = [
        CandidatePreferredIndustryInline,
        CandidatePreferredOccupationInline,
        CandidatePreferredLocationInline,
    ]

    list_display: ClassVar = [
        "id",
        "media",
        "id_in_media",
        "current_company",
    ]

    list_display_links: ClassVar = [
        "id_in_media",
    ]

    readonly_fields: ClassVar = [
        "id",
        "last_name",
        "first_name",
        "gender",
        "age",
        "prefecture",
        "industry",
        "occupation",
        "position",
        "current_company",
        "department",
        "job_title",
        "current_annual_income_min",
        "current_annual_income_max",
        "work_value_1",
        "work_value_2",
        "expectation_1",
        "expectation_2",
        "dissatisfaction_1",
        "dissatisfaction_2",
        "anxiety_1",
        "anxiety_2",
        "is_career_change",
        "preferred_annual_income",
    ]

    form = CandidateCreateForm

    def get_form(self, request, obj=None, **kwargs):
        # フォームに user を追加して渡す
        form = super().get_form(request, obj, **kwargs)
        form.user = request.user

        return form

    def change_view(
            self,
            request,
            object_id: int,
            form_url: str='',
            extra_context: (dict|None)=None
        ) :
        """
        候補者詳細画面をカスタマイズ（各種リンクの追加）
        """  # noqa: RUF002
        extra_context = extra_context or {}

        # 学歴一覧へのリンクを追加
        link_achademic_history = reverse(
            "admin:base_candidateacademichistory_changelist"
        ) + f'?candidate__id__exact={object_id}'
        extra_context['link_achademic_history'] = format_html(
            '<a href="{}">学歴</a>', link_achademic_history
        )

        # 職務経歴一覧へのリンクを追加
        link_work_history = reverse(
            "admin:base_candidateworkhistory_changelist"
            ) + f'?candidate__id__exact={object_id}'
        extra_context['link_work_history'] = format_html(
            '<a href="{}">職務経歴</a>', link_work_history
        )

        # 資格一覧へのリンクを追加
        link_certification = reverse(
            "admin:base_candidatecertification_changelist"
            ) + f'?candidate__id__exact={object_id}'
        extra_context['link_certification'] = format_html(
            '<a href="{}">資格</a>', link_certification
        )

        # スキル一覧へのリンクを追加
        link_skill = reverse(
            "admin:base_candidateskill_changelist"
            ) + f'?candidate__id__exact={object_id}'
        extra_context['link_skill'] = format_html(
            '<a href="{}">スキル</a>', link_skill
        )

        # スカウト詳細へのリンクを追加
        scout = Scout.objects.filter(candidate__id=object_id).first()
        link_scout = reverse("admin:base_scout_change", args=[scout.id])
        extra_context['link_scout'] = format_html(
            '<a href="{}">スカウトメール</a>', link_scout
        )

        return super().change_view(request, object_id, form_url, extra_context=extra_context)



####################################################################
# Linked Model
####################################################################
@admin.register(CandidateAcademicHistory)
class CandidateAcademicHistoryAdmin(admin.ModelAdmin):
    """
    (管理画面設定) 候補者学歴
    """

    list_display: ClassVar = [
        "candidate",
        "enrollment_date",
        "graduation_date",
        "school",
        "department",
    ]

@admin.register(CandidateWorkHistory)
class CandidateWorkHistoryAdmin(admin.ModelAdmin):
    """
    (管理画面設定) 候補者職歴
    """

@admin.register(CandidateSkill)
class CandidateSkillAdmin(admin.ModelAdmin):
    """
    (管理画面設定) 候補者スキル
    """

@admin.register(CandidateCertification)
class CandidateCertificationAdmin(admin.ModelAdmin):
    """
    (管理画面設定) 候補者資格
    """


# @admin.register(CandidatePreferredIndustry)
# class CandidatePreferredIndustryAdmin(admin.ModelAdmin):
#     """
#     (管理画面設定) 候補者希望業界
#     """

# @admin.register(CandidatePreferredOccupation)
# class CandidatePreferredOccupationAdmin(admin.ModelAdmin):
#     """
#     (管理画面設定) 候補者希望職種
#     """

# @admin.register(CandidatePreferredLocation)
# class CandidatePreferredLocationAdmin(admin.ModelAdmin):
#     """
#     (管理画面設定) 候補者希望勤務地
#     """
