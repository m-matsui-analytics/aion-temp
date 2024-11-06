from django.db import models

from .base import BaseModel


class CandidateAcademicHistory(BaseModel):
    """
    候補者の学歴モデル

    | カラム名         | カラム名（日本語） | データ型     | NULL設定     | 外部キー     | ユニークキー |
    |------------------|-------------------|--------------|--------------|--------------|--------------|
    | id               | ID                | int          | NOT NULL     |              |              |
    | candidate_id     | 候補者ID          | int          | NOT NULL     | candidates   |              |
    | enrollment_date  | 入学日            | date         | NULL         |              |              |
    | graduation_date  | 卒業日            | date         | NULL         |              |              |
    | school           | 学校              | varchar(255) | NOT NULL     |              |              |
    | department       | 学部・学科        | varchar(255) | NOT NULL("") |              |              |
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

    enrollment_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="入学日"
    )

    graduation_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="卒業日"
    )

    school = models.CharField(
        blank=True,
        null=False,
        max_length=255,
        verbose_name="学校"
    )

    department = models.CharField(
        blank=True,
        null=False,
        default="",
        max_length=255,
        verbose_name="学部・学科"
    )


    class Meta: # noqa: D106
        db_table = "candidate_academic_histories"
        verbose_name = verbose_name_plural = "候補者の学歴"
        app_label = 'base'

    def __str__(self) -> str: # noqa: D105
        return f"{self.candidate} {self.school}"
