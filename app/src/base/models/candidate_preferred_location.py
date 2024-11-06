from typing import ClassVar

from django.db import models

from .base import BaseModel
from .choices import Prefecture


class CandidatePreferredLocation(BaseModel):
    """
    候補者の希望勤務地モデル

    | カラム名      | カラム名（日本語）  | データ型    | NULL設定   | 外部キー     | ユニークキー |
    |---------------|--------------------|-------------|------------|--------------|--------------|
    | id            | ID                 | int         | NOT NULL   |              |              |
    | candidate_id  | 候補者ID           | int         | NOT NULL   | candidates   |              |
    | location      | 希望勤務地         | int         | NOT NULL   |              |              |
    | created_at    | 作成日時           | datetime    | NOT NULL   |              |              |
    | updated_at    | 更新日時           | datetime    | NOT NULL   |              |              |

    複合キー:
    | 名称                | カラム                        |
    |---------------------|-------------------------------|
    | candidate_location  | ・candidate_id<br>・location  |

    """  # noqa: E501, RUF002

    candidate = models.ForeignKey(
        "Candidate",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="候補者"
    )

    location = models.SmallIntegerField(
        blank=False,
        null=False,
        choices=Prefecture.choices,
        verbose_name="希望勤務地"
    )


    class Meta: # noqa: D106
        db_table = "candidate_preferred_locations"
        verbose_name = verbose_name_plural = "希望勤務地"
        constraints: ClassVar = [
            models.UniqueConstraint(
                fields=["candidate", "location"],
                name="candidate_location"
            )
        ]
        app_label = 'base'

    def __str__(self) -> str: # noqa: D105
        return f"{self.candidate} {self.get_location_display()}"
