from django.db import models

from .base import BaseModel
from .choices import RelevanceLevel


class CompanyStrengthRA(BaseModel):
    """
    企業の強み-採用記事モデル

    | カラム名               | カラム名（日本語）   | データ型      | NULL設定   | 外部キー             | ユニークキー |
    |------------------------|---------------------|---------------|------------|----------------------|--------------|
    | id                     | ID                  | int           | NOT NULL   |                      |              |
    | strength_id            | 企業の強みID        | int           | NOT NULL   | strengths            |              |
    | recruitment_article_id | 採用記事ID    | int           | NOT NULL   | recruitment_articles |              |
    | created_at             | 作成日時            | datetime      | NOT NULL   |                      |              |
    | updated_at             | 更新日時            | datetime      | NOT NULL   |                      |              |
    | deleted_at             | 削除日時            | datetime      | NULL       |                      |              |

    """  # noqa: E501, RUF002

    strength = models.ForeignKey(
        "CompanyStrength",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="企業の強み",
    )

    recruitment_article = models.ForeignKey(
        "RecruitmentArticle",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="採用記事",
    )

    relevance_level = models.SmallIntegerField(
        blank=True,
        null=True,
        choices=RelevanceLevel.choices,
        verbose_name="関連度",
    )

    class Meta:  # noqa: D106
        db_table = "company_strength_ras"
        verbose_name = verbose_name_plural = "求める人物像-採用記事"
        app_label = "base"

    def __str__(self) -> str:  # noqa: D105
        return self.strength.strength + self.recruitment_article.title
