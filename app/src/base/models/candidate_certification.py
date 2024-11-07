from django.db import models

from .base import BaseModel


class CandidateCertification(BaseModel):
    """
    候補者の資格モデル

    | カラム名         | カラム名（日本語） | データ型     | NULL設定     | 外部キー     | ユニークキー |
    |------------------|-------------------|--------------|--------------|--------------|--------------|
    | id               | ID                | int          | NOT NULL     |              |              |
    | candidate_id     | 候補者ID          | int          | NOT NULL     | candidates   |              |
    | acquisition_date | 取得日            | date         | NULL         |              |              |
    | certification    | 資格              | varchar(255) | NOT NULL("") |              |              |
    | created_at       | 作成日時          | datetime     | NOT NULL     |              |              |
    | updated_at       | 更新日時          | datetime     | NOT NULL     |              |              |

    """  # noqa: E501, RUF002

    candidate = models.ForeignKey(
        "Candidate",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="候補者"
    )

    acquisition_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="取得日"
    )

    certification = models.CharField(
        blank=True,
        null=False,
        default="",
        max_length=255,
        verbose_name="資格"
    )


    class Meta: # noqa: D106
        db_table = "candidate_certifications"
        verbose_name = verbose_name_plural = "候補者の資格"
        app_label = 'base'

    def __str__(self) -> str: # noqa: D105
        return self.certification
