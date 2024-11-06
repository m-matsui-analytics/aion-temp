from typing import ClassVar

from django.contrib import admin

from base.models import (
    Scout,
    ScoutMail,
)


####################################################################
# InlineModel
####################################################################
class ScoutMailInline(admin.StackedInline):
    """
    (管理画面設定) スカウトメール
    """

    model = ScoutMail
    extra = 0

    fields: ClassVar = [
        "empathy_emotion",
        "strength_1",
        "strength_2",
        "strength_3",
        "job_posting",
        "recruitment_article_1",
        "recruitment_article_2",
        "recruitment_article_3",
        "scout_sender",
        "subject",
        "body",
    ]

# class ScoutMailInline(admin.TabularInline):
#     """
#     (管理画面設定) スカウトメール
#     """

#     model = ScoutMail
#     extra = 0

@admin.register(Scout)
class ScoutAdmin(admin.ModelAdmin):
    """
    (管理画面設定) スカウト
    """

    inlines: ClassVar = [
        ScoutMailInline,
    ]

    list_display: ClassVar = [
        "candidate",
    ]

    fields: ClassVar = [
        "candidate",
        "ideal_candidate",
        "matching_rate",
        "is_matched",
        "reason",
    ]
