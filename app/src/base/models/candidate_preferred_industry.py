from typing import ClassVar

from django.db import models

from .base import BaseModel
from .choices import Industry


class CandidatePreferredIndustry(BaseModel):
    """
    候補者の希望業種モデル

    | カラム名      | カラム名（日本語）  | データ型    | NULL設定   | 外部キー     | ユニークキー |
    |---------------|--------------------|-------------|------------|--------------|--------------|
    | id            | ID                 | int         | NOT NULL   |              |              |
    | candidate_id  | 候補者ID           | int         | NOT NULL   | candidates   |              |
    | industry      | 希望               | int         | NOT NULL   |              |              |
    | created_at    | 作成日時           | datetime    | NOT NULL   |              |              |
    | updated_at    | 更新日時           | datetime    | NOT NULL   |              |              |

    複合キー:
    | 名称                | カラム                        |
    |---------------------|-------------------------------|
    | candidate_industry  | ・candidate_id<br>・industry  |

    """  # noqa: E501, RUF002

    candidate = models.ForeignKey(
        "Candidate",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="候補者"
    )

    industry = models.SmallIntegerField(
        blank=False,
        null=False,
        choices=Industry.choices,
        verbose_name="希望業種"
    )


    class Meta: # noqa: D106
        db_table = "candidate_preferred_industries"
        verbose_name = verbose_name_plural = "希望業種"
        constraints: ClassVar = [
            models.UniqueConstraint(
                fields=["candidate", "industry"],
                name="candidate_industry"
            )
        ]
        app_label = 'base'

    def __str__(self) -> str: # noqa: D105
        return f"{self.candidate} {self.get_industry_display()}"
