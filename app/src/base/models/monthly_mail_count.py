from django.db import models

from .base import BaseModel


class MonthlyMailCount(BaseModel):
    """
    月間メール作成数モデル

    | カラム名     | カラム名（日本語）  | データ型      | NULL設定   | 外部キー   | ユニークキー |
    |--------------|--------------------|---------------|------------|------------|--------------|
    | id           | ID                 | int           | NOT NULL   |            |              |
    | company_id   | 企業ID             | int           | NOT NULL   | companies  |              |
    | year_month   | 年月               | date          | NOT NULL   |            |              |
    | count        | 作成数             | int           | NOT NULL(0)|            |              |
    | created_at   | 作成日時           | datetime      | NOT NULL   |            |              |
    | updated_at   | 更新日時           | datetime      | NOT NULL   |            |              |
    | deleted_at   | 削除日時           | datetime      | NULL       |            |              |
    """  # noqa: E501, RUF002

    company = models.ForeignKey(
        "Company",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        verbose_name="企業"
    )

    year_month = models.DateField(
        blank=False,
        null=False,
        verbose_name="年月"
    )

    count = models.IntegerField(
        blank=False,
        null=False,
        default=0,
        verbose_name="作成数"
    )


    class Meta: # noqa: D106
        db_table = "monthly_mail_counts"
        verbose_name = verbose_name_plural = "月間メール作成数"
        app_label = "base"

    def __str__(self) -> str: # noqa: D105
        return self.name
