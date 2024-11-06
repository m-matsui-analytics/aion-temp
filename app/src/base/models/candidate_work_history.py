from django.db import models

from .base import BaseModel


class CandidateWorkHistory(BaseModel):
    """
    候補者の職務経歴モデル

    | カラム名      | カラム名（日本語）  | データ型    | NULL設定     | 外部キー     | ユニークキー |
    |---------------|--------------------|-------------|--------------|--------------|--------------|
    | id            | ID                 | int         | NOT NULL     |              |              |
    | candidate_id  | 候補者ID           | int         | NOT NULL     | candidates   |              |
    | start_date    | 開始日             | date        | NULL         |              |              |
    | end_date      | 終了日             | date        | NULL         |              |              |
    | experience    | 経験               | text        | NOT NULL("") |              |              |
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

    start_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="開始日"
    )

    end_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="終了日"
    )

    # 企業名
    # 部署名

    experience = models.TextField(
        blank=True,
        null=False,
        default="",
        verbose_name="概要"
    )

    detail = models.TextField(
        blank=True,
        null=False,
        default="",
        verbose_name="詳細"
    )


    class Meta: # noqa: D106
        db_table = "candidate_work_histories"
        verbose_name = verbose_name_plural = "候補者の職務経歴"
        app_label = 'base'

    def __str__(self) -> str: # noqa: D105
        return f"{self.candidate} {self.experience}"
