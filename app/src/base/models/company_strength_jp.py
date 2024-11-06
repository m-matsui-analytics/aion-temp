from django.db import models

from .base import BaseModel
from .choices import RelevanceLevel


class CompanyStrengthJP(BaseModel):
    """
    企業の強み-求人票モデル

    | カラム名               | カラム名（日本語）   | データ型      | NULL設定   | 外部キー      | ユニークキー |
    |------------------------|---------------------|---------------|------------|---------------|--------------|
    | id                     | ID                  | int           | NOT NULL   |               |              |
    | strength_id            | 企業の強みID        | int           | NOT NULL   | strengths     |              |
    | job_posting_id         | 求人票ID            | int           | NOT NULL   | job_postings  |              |
    | created_at             | 作成日時            | datetime      | NOT NULL   |               |              |
    | updated_at             | 更新日時            | datetime      | NOT NULL   |               |              |
    | deleted_at             | 削除日時            | datetime      | NULL       |               |              |

    """  # noqa: E501, RUF002

    strength = models.ForeignKey(
        "CompanyStrength",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="企業の強み",
    )

    job_posting = models.ForeignKey(
        "JobPosting",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="求人票",
    )

    relevance_level = models.SmallIntegerField(
        blank=True,
        null=True,
        choices=RelevanceLevel.choices,
        verbose_name="関連度",
    )

    class Meta:  # noqa: D106
        db_table = "company_strength_jps"
        verbose_name = verbose_name_plural = "企業の強み-求人票"
        app_label = "base"

    def __str__(self) -> str:  # noqa: D105
        return self.strength.strength + self.job_posting.title
