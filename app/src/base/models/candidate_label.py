from django.db import models

from .base import BaseModel


class CandidateLabel(BaseModel):
    """
    候補者-ラベルモデル

    | カラム名               | カラム名（日本語）   | データ型      | NULL設定   | 外部キー      | ユニークキー |
    |------------------------|---------------------|---------------|------------|---------------|--------------|
    | id                     | ID                  | int           | NOT NULL   |               |              |
    | candidate_id           | 候補者ID            | int           | NOT NULL   | candidates    |              |
    | label_id               | ラベルID            | int           | NOT NULL   | labels        |              |
    | created_at             | 作成日時            | datetime      | NOT NULL   |               |              |
    | updated_at             | 更新日時            | datetime      | NOT NULL   |               |              |
    | deleted_at             | 削除日時            | datetime      | NULL       |               |              |

    """  # noqa: E501, RUF002

    candidate = models.ForeignKey(
        "Candidate",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="候補者",
    )

    label = models.ForeignKey(
        "Label",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="ラベル",
    )


    class Meta:  # noqa: D106
        db_table = "candidate_labels"
        verbose_name = verbose_name_plural = "候補者-ラベル"
        app_label = 'base'

    # def __str__(self) -> str:  # noqa: D105
    #     return self.candidate + self.label.label
