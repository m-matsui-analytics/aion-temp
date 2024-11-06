
from typing import ClassVar

from django.core.exceptions import ValidationError
from django.db import models

from .base import BaseModel
from .choices import HTMLContentAnalysisStatus, RecruitmentMedia


class RecruitmentArticle(BaseModel):
    """
    採用記事モデル

    | カラム名      | カラム名（日本語）  | データ型      | NULL設定   | 外部キー            | ユニークキー |
    |---------------|--------------------|---------------|------------|---------------------|--------------|
    | id            | ID                 | int           | NOT NULL   |                     |              |
    | company_id    | 企業ID             | int           | NOT NULL   | companies           |              |
    | name          | 採用記事名             | varchar(255)  | NOT NULL   |                     |              |
    | url           | URL                | text          | NOT NULL   |                     |             |
    | media_id      | 採用媒体ID         | int           | NOT NULL   | recruitment-medias  |              |
    | summary       | 要約               | text          | NOT NULL("")  |                     |              |
    | created_at    | 作成日時           | datetime      | NOT NULL   |                     |              |
    | updated_at    | 更新日時           | datetime      | NOT NULL   |                     |              |
    | deleted_at    | 削除日時           | datetime      | NULL       |                     |              |
    ※ urlカラムをユニークにしたかったが、text型はユニークキーに設定できないためsave時にバリデーションを行う

    """  # noqa: E501, RUF002

    company = models.ForeignKey(
        "Company",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="企業"
    )

    title = models.CharField(
        blank=True,
        null=False,
        max_length=255,
        default="",
        verbose_name="タイトル"
    )

    url = models.URLField(
        blank=True,
        null=False,
        verbose_name="URL"
    )

    media = models.SmallIntegerField(
        blank=False,
        null=False,
        choices=RecruitmentMedia.choices,
        verbose_name="採用媒体"
    )

    summary = models.TextField(
        blank=True,
        null=False,
        default="",
        verbose_name="要約"
    )

    analysis_status = models.SmallIntegerField(
        blank=True,
        null=False,
        choices=HTMLContentAnalysisStatus.choices,
        default=HTMLContentAnalysisStatus.IN_PROGRESS,
        verbose_name="解析状況"
    )


    class Meta:  # noqa: D106
        db_table = "recruitment_articles"
        verbose_name = verbose_name_plural = "採用記事"
        app_label = "base"
        constraints: ClassVar= [
            models.UniqueConstraint(
                fields=["company", "url"],
                name="company_url_ra"
            )
        ]

    def __str__(self) -> str:  # noqa: D105
        return str(self.id) + ": " + self.title

    def save(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """作成・追加時の前処理を追加"""
        self.clean()
        super().save(*args, **kwargs)
