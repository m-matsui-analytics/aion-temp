from django.db import models

from .base import BaseModel
from .choices import RequirementCategory, RequirementLevel


class IdealCandidateRequirement(BaseModel):
    """
    求める人物像要件モデル

    | カラム名               | カラム名（日本語）   | データ型      | NULL設定   | 外部キー             | ユニークキー |
    |------------------------|---------------------|---------------|------------|----------------------|--------------|
    | id                     | ID                  | int           | NOT NULL   |                      |              |
    | ideal_candidate_id     | 求める人物像ID      | int           | NOT NULL   | ideal_candidates     |              |
    | requirement_category   | 要件カテゴリ        | int           | NOT NULL   |                      |              |
    | requirement            | 要件                | varchar(200)  | NOT NULL   |                      |              |
    | requirement_level      | 要件レベルID        | small_int     | NOT NULL   |                      |              |
    | created_at             | 作成日時            | datetime      | NOT NULL   |                      |              |
    | updated_at             | 更新日時            | datetime      | NOT NULL   |                      |              |
    | deleted_at             | 削除日時            | datetime      | NULL       |                      |              |

    """  # noqa: E501, RUF002

    ideal_candidate = models.ForeignKey(
        "IdealCandidate",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="求める人物像",
    )

    requirement_category = models.SmallIntegerField(
        blank=False,
        null=False,
        choices=RequirementCategory.choices,
        verbose_name="要件カテゴリ",
    )

    requirement = models.CharField(
        blank=False,
        null=False,
        max_length=255,
        verbose_name="要件"
    )

    requirement_level = models.SmallIntegerField(
        blank=False,
        null=False,
        choices=RequirementLevel.choices,
        verbose_name="要件レベル",
    )


    class Meta:  # noqa: D106
        db_table = "ideal_candidate_requirements"
        verbose_name = verbose_name_plural = "求める人物像要件"
        app_label = "base"

    def __str__(self) -> str:  # noqa: D105
        return self.recruitment
