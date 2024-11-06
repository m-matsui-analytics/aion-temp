from django.db import models

from .base import BaseModel
from .choices import (
    Education,
    EmploymentStatus,
    Industry,
    Occupation,
    Position,
    RangeType,
)


class IdealCandidate(BaseModel):
    """
    求める人物像モデル

    | カラム名              | カラム名（日本語）   | データ型      | NULL設定   | 外部キー      | ユニークキー |
    |-----------------------|---------------------|---------------|------------|---------------|--------------|
    | id                    | ID                  | int           | NOT NULL   |               |              |
    | company_id            | 企業ID              | int           | NOT NULL   | companies     |              |
    | name                  | 人物像名            | char(255)     | NOT NULL   |               |              |
    | age_min               | 年齢（下限）        | small_int     | NULL       |               |              |
    | age_max               | 年齢（上限）        | small_int     | NULL       |               |              |
    | education             | 学歴                | small_int     | NULL       |               |              |
    | preferred_industry    | 希望業界            | int           | NULL       | industries    |              |
    | preferred_occupation  | 希望職種            | small_int     | NULL       |               |              |
    | current_position      | 現在の役職          | small_int     | NULL       |               |              |
    | current_annual_income | 直近の年収（万円）  | int           | NULL       |               |              |
    | income_range_type     | 年収の範囲          | small_int     | NULL       |               |              |
    | employment_status     | 就業状況            | small_int     | NULL       |               |              |
    | work_value_1          | 仕事観1             | int           | NULL       | work_values   |              |
    | work_value_2          | 仕事観2             | int           | NULL       | work_values   |              |
    | work_value_3          | 仕事観3             | int           | NULL       | work_values   |              |
    | created_at            | 作成日時            | datetime      | NOT NULL   |               |              |
    | updated_at            | 更新日時            | datetime      | NOT NULL   |               |              |
    | deleted_at            | 削除日時            | datetime      | NULL       |               |              |

    """  # noqa: E501, RUF002

    company = models.ForeignKey(
        "Company",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="企業",
    )

    name = models.CharField(
        blank=False,
        null=False,
        max_length=255,
        verbose_name="人物像名"
    )

    age_min = models.SmallIntegerField(
        blank=True,
        null=True,
        verbose_name="年齢（下限）")  # noqa: RUF001

    age_max = models.SmallIntegerField(
        blank=True,
        null=True,
        verbose_name="年齢（上限）")  # noqa: RUF001

    education = models.SmallIntegerField(
        blank=True,
        null=True,
        choices=Education.choices,
        verbose_name="学歴"
    )

    preferred_industry = models.IntegerField(
        blank=True,
        null=True,
        choices=Industry.choices,
        verbose_name="希望業種"
    )

    preferred_occupation = models.SmallIntegerField(
        blank=True,
        null=True,
        choices=Occupation.choices,
        verbose_name="希望職種"
    )

    current_position = models.SmallIntegerField(
        blank=True,
        null=True,
        choices=Position.choices,
        verbose_name="現在の役職"
    )

    current_annual_income = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="直近の年収（万円）" # noqa: RUF001
    )

    current_income_range_type = models.SmallIntegerField(
        blank=True,
        null=True,
        choices=RangeType.choices,
        verbose_name="年収の範囲タイプ"
    )

    desired_annual_income = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="希望年収（万円）" # noqa: RUF001
    )

    desired_income_range_type = models.SmallIntegerField(
        blank=True,
        null=True,
        choices=RangeType.choices,
        verbose_name="希望年収の範囲タイプ"
    )

    employment_status = models.SmallIntegerField(
        blank=True,
        null=True,
        choices=EmploymentStatus.choices,
        verbose_name="就業状況"
    )

    work_value_1 = models.ForeignKey(
        "WorkValue",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="dc_work_value_1",
        verbose_name="仕事観1"
    )

    work_value_2 = models.ForeignKey(
        "WorkValue",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="dc_work_value_2",
        verbose_name="仕事観2"
    )

    work_value_3 = models.ForeignKey(
        "WorkValue",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="dc_work_value_3",
        verbose_name="仕事観3"
    )

    job_postings = models.ManyToManyField(
        "JobPosting",
        through="IdealCandidateJP",
        verbose_name="求人票",
    )

    recruitment_articles = models.ManyToManyField(
        "RecruitmentArticle",
        through="IdealCandidateRA",
        verbose_name="採用記事",
    )

    class Meta:  # noqa: D106
        db_table = "ideal_candidates"
        verbose_name = verbose_name_plural = "求める人物像"
        app_label = "base"

    def __str__(self) -> str:  # noqa: D105
        return self.name
