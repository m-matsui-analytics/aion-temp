from typing import ClassVar

from django.db import models

from .base import BaseModel


class KPI(BaseModel):
    """
    KPIモデル

    | カラム名           | カラム名（日本語）  | データ型    | NULL設定   | 外部キー   | ユニークキー |
    |--------------------|--------------------|-------------|------------|------------|--------------|
    | id                 | ID                 | int         | NOT NULL   |            |              |
    | company_id         | 企業ID             | int         | NOT NULL   | companies  |              |
    | year               | 年                 | small_int   | NOT NULL   |            |              |
    | month              | 月                 | small_int   | NULL       |            |              |
    | recruitment_total  | 採用総数           | int         | NULL       |            |              |
    | recruitment_dr     | DR採用数           | int         | NULL       |            |              |
    | scout_send_counts  | スカウト送信数     | int         | NULL       |            |              |
    | scout_reply_counts | スカウト返信数     | int         | NULL       |            |              |
    | scout_mtg_counts   | 面談設定数         | int         | NULL       |            |              |
    | created_at         | 作成日時           | datetime    | NOT NULL   |            |              |
    | updated_at         | 更新日時           | datetime    | NOT NULL   |            |              |
    | deleted_at         | 削除日時           | datetime    | NULL       |            |              |

    複合キー:
    | 名称               | カラム                          |
    |--------------------|---------------------------------|
    | company_year_month  | ・company_id<br>・year<br>・month |
    """  # noqa: E501, RUF002

    company = models.ForeignKey(
        "Company",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="企業"
    )

    year = models.SmallIntegerField(
        blank=False,
        null=False,
        verbose_name="年"
    )

    month = models.SmallIntegerField(
        blank=True,
        null=True,
        verbose_name="月"
    )

    recruitment_total = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="採用総数"
    )

    recruitment_dr = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="DR採用数"
    )

    scout_send_counts = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="スカウト送信数"
    )

    scout_reply_counts = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="スカウト返信数"
    )

    scout_mtg_counts = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="面談設定数"
    )


    class Meta: # noqa: D106
        db_table = "kpis"
        verbose_name = verbose_name_plural = "KPI"
        constraints: ClassVar= [
            models.UniqueConstraint(
                fields=["company", "year", "month"],
                name="company_year_month"
            )
        ]
        app_label = "base"

    def __str__(self) -> str: # noqa: D105
        return self.company + self.year + self.month
