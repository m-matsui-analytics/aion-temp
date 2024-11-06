from django.db import models

from .base import BaseModel


class CompanyStrength(BaseModel):
    """
    企業の強みモデル

    | カラム名      | カラム名（日本語）  | データ型      | NULL設定      | 外部キー   | ユニークキー |
    |---------------|--------------------|---------------|--------------|------------|--------------|
    | id            | ID                 | int           | NOT NULL     |            |              |
    | company_id    | 企業ID             | int           | NOT NULL     | companies  |              |
    | strength  | 強み               | varchar(200)  | NOT NULL     |            |              |
    | description   | 説明               | text          | NOT NULL('') |            |              |
    | created_at    | 作成日時           | datetime      | NOT NULL     |            |              |
    | updated_at    | 更新日時           | datetime      | NOT NULL     |            |              |
    | deleted_at    | 削除日時           | datetime      | NULL         |            |              |

    """  # noqa: E501, RUF002

    company = models.ForeignKey(
        "Company",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="企業",
    )

    strength = models.CharField(
        blank=False,
        null=False,
        max_length=255,
        verbose_name="強み"
    )

    description = models.TextField(
        blank=True,
        null=False,
        default="",
        verbose_name="説明"
    )

    job_postings = models.ManyToManyField(
        "JobPosting",
        through="CompanyStrengthJP",
        verbose_name="求人票",
    )

    recruitment_articles = models.ManyToManyField(
        "RecruitmentArticle",
        through="CompanyStrengthRA",
        verbose_name="採用記事",
    )

    class Meta:  # noqa: D106
        db_table = "company_strengths"
        verbose_name = verbose_name_plural = "企業の強み"
        app_label = "base"

    def __str__(self) -> str:  # noqa: D105
        return self.strength
