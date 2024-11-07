from django.db import models

from .base import BaseModel


class CandidateSkill(BaseModel):
    """
    候補者のスキルモデル

    | カラム名      | カラム名（日本語）  | データ型    | NULL設定     | 外部キー     | ユニークキー |
    |---------------|--------------------|-------------|--------------|--------------|--------------|
    | id            | ID                 | int         | NOT NULL     |              |              |
    | candidate_id  | 候補者ID           | int         | NOT NULL     | candidates   |              |
    | duration      | 期間（年）         | int         | NULL         |              |              |
    | skill         | 経験年数           | text        | NOT NULL("") |              |              |
    | detail        | 詳細               | text        | NOT NULL("") |              |              |
    | created_at    | 作成日時           | datetime    | NOT NULL     |              |              |
    | updated_at    | 更新日時           | datetime    | NOT NULL     |              |              |

    """  # noqa: E501, RUF002

    candidate = models.ForeignKey(
        "Candidate",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="候補者"
    )

    duration = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="期間"
    )

    skill = models.TextField(
        blank=True,
        null=False,
        default="",
        verbose_name="スキル"
    )

    detail = models.TextField(
        blank=True,
        null=False,
        default="",
        verbose_name="詳細"
    )


    class Meta: # noqa: D106
        db_table = "candidate_skills"
        verbose_name = verbose_name_plural = "候補者のスキル"
        app_label = 'base'

    def __str__(self) -> str: # noqa: D105
        return self.skill
