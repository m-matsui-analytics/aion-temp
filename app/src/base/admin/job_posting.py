from typing import ClassVar

from django import forms
from django.contrib import admin
from django.urls import path

from base.forms import JobPostingTextCreateForm
from base.models import JobPosting


# @admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    """
    (管理画面設定) 採用記事
    """

    list_display: ClassVar = [
        "id",
        "company",
        "media",
        "title",
    ]

    form = JobPostingTextCreateForm

    def get_form(self, request, obj=None, **kwargs):
        # フォームに user を追加して渡す
        form = super().get_form(request, obj, **kwargs)
        form.user = request.user

        print(f"request.user: {request.user}")
        return form

admin.site.register(JobPosting, JobPostingAdmin)
