##################################################################
# テストデータ作成用に適当に作成
##################################################################

from typing import ClassVar

from django.contrib import admin

from base.models import (
    KPI,
    Candidate,
    CandidateAcademicHistory,
    CandidateCertification,
    CandidateFeeling,
    CandidateLabel,
    CandidatePreferredIndustry,
    CandidatePreferredLocation,
    CandidateSkill,
    CandidateWorkHistory,
    Company,
    CompanyInfo,
    CompanyMedia,
    CompanyStrength,
    CompanyStrengthJP,
    CompanyStrengthRA,
    IdealCandidate,
    IdealCandidateJP,
    IdealCandidateRA,
    IdealCandidateRequirement,
    Label,
    MailGenLog,
    MonthlyMailCount,
    Scout,
    ScoutMail,
    ScoutSender,
    WorkValue,
)


# @admin.register(CandidateAcademicHistory)
# class CandidateAcademicHistoryAdmin(admin.ModelAdmin):
#     """
#     (管理画面設定) 候補者学歴
#     """

# @admin.register(CandidateCertification)
# class CandidateCertificationAdmin(admin.ModelAdmin):
#     """
#     (管理画面設定) 候補者資格
#     """

@admin.register(CandidateFeeling)
class CandidateFeelingAdmin(admin.ModelAdmin):
    """
    (管理画面設定) 候補者志向
    """

    list_display: ClassVar = [
        "emotion_type",
        "feeling",
        "is_disabled",
    ]

@admin.register(CandidateLabel)
class CandidateLabelAdmin(admin.ModelAdmin):
    """
    (管理画面設定) 候補者ラベル
    """

# @admin.register(CandidatePreferredIndustry)
# class CandidatePreferredIndustryAdmin(admin.ModelAdmin):
#     """
#     (管理画面設定) 候補者希望業界
#     """

# @admin.register(CandidatePreferredLocation)
# class CandidatePreferredLocationAdmin(admin.ModelAdmin):
#     """
#     (管理画面設定) 候補者希望勤務地
#     """

# @admin.register(CandidateSkill)
# class CandidateSkillAdmin(admin.ModelAdmin):
#     """
#     (管理画面設定) 候補者スキル
#     """

# @admin.register(CandidateWorkHistory)
# class CandidateWorkHistoryAdmin(admin.ModelAdmin):
#     """
#     (管理画面設定) 候補者職歴
#     """

# @admin.register(Candidate)
# class CandidateAdmin(admin.ModelAdmin):
#     """
#     (管理画面設定) 候補者
#     """

@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    """
    (管理画面設定) 企業情報
    """

@admin.register(CompanyMedia)
class CompanyMediaAdmin(admin.ModelAdmin):
    """
    (管理画面設定) 企業メディア
    """

@admin.register(CompanyStrengthJP)
class CompanyStrengthJPAdmin(admin.ModelAdmin):
    """
    (管理画面設定) 企業強みJP
    """

@admin.register(CompanyStrengthRA)
class CompanyStrengthRAAdmin(admin.ModelAdmin):
    """
    (管理画面設定) 企業強みRA
    """

@admin.register(CompanyStrength)
class CompanyStrengthAdmin(admin.ModelAdmin):
    """
    (管理画面設定) 企業強み
    """

    list_display: ClassVar = [
        "company",
        "strength",
    ]

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """
    (管理画面設定) 企業
    """

@admin.register(IdealCandidateJP)
class IdealCandidateJPAdmin(admin.ModelAdmin):
    """
    (管理画面設定) 理想の候補者JP
    """

@admin.register(IdealCandidateRA)
class IdealCandidateRAAdmin(admin.ModelAdmin):
    """
    (管理画面設定) 理想の候補者RA
    """

@admin.register(IdealCandidateRequirement)
class IdealCandidateRequirementAdmin(admin.ModelAdmin):
    """
    (管理画面設定) 理想の候補者要件
    """

    list_display: ClassVar = [
        "ideal_candidate",
        "requirement_level",
        "requirement_category",
        "requirement",
    ]

@admin.register(IdealCandidate)
class IdealCandidateAdmin(admin.ModelAdmin):
    """
    (管理画面設定) 理想の候補者
    """

    list_display: ClassVar = [
        "id",
        "company",
        "name",
    ]

# @admin.register(JobPosting)
# class JobPostingAdmin(admin.ModelAdmin):
#     """
#     (管理画面設定) 求人
#     """

@admin.register(KPI)
class KPIAdmin(admin.ModelAdmin):
    """
    (管理画面設定) KPI
    """

@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    """
    (管理画面設定) ラベル
    """

@admin.register(MailGenLog)
class MailGenLogAdmin(admin.ModelAdmin):
    """
    (管理画面設定) メール生成ログ
    """

    list_display:ClassVar = [
        "id",
        "candidate_id",  # candidate表示用のカスタムメソッドを追加
        "scout",
        "scout_mail",
        "created_at",
    ]
    # candidateを表示するカスタムメソッド
    def candidate_id(self, obj):
        # scout経由でcandidateにアクセスし、候補者名を返す
        return obj.scout.candidate.id if obj.scout and obj.scout.candidate else "-"
    candidate_id.short_description = "Candidate"

@admin.register(MonthlyMailCount)
class MonthlyMailCountAdmin(admin.ModelAdmin):
    """
    (管理画面設定) 月間メール送信数
    """

# @admin.register(ScoutMail)
# class ScoutMailAdmin(admin.ModelAdmin):
#     """
#     (管理画面設定) スカウトメール
#     """

@admin.register(ScoutSender)
class ScoutSenderAdmin(admin.ModelAdmin):
    """
    (管理画面設定) スカウト送信者
    """
    list_display: ClassVar = [
        "company",
        "name",
        "department",
        "position",
        "gender",
    ]
# @admin.register(Scout)
# class ScoutAdmin(admin.ModelAdmin):
#     """
#     (管理画面設定) スカウト
#     """

@admin.register(WorkValue)
class WorkValueAdmin(admin.ModelAdmin):
    """
    (管理画面設定) 企業価値観
    """


