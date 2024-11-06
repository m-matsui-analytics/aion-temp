from typing import ClassVar

from django import forms
from django.contrib import admin
from django.urls import path

from base.forms import RecruitmentArticleTextCreateForm
from base.models import RecruitmentArticle


# @admin.register(RecruitmentArticle)
class RecruitmentArticleAdmin(admin.ModelAdmin):
    """
    (管理画面設定) 採用記事
    """

    list_display: ClassVar = [
        "id",
        "company",
        "media",
        "title",
    ]

    form = RecruitmentArticleTextCreateForm

    def get_form(self, request, obj=None, **kwargs):
        # フォームに user を追加して渡す
        form = super().get_form(request, obj, **kwargs)
        form.user = request.user

        print(f"request.user: {request.user}")
        return form

admin.site.register(RecruitmentArticle, RecruitmentArticleAdmin)
