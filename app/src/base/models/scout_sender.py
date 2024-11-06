from django.db import models

from .base import BaseModel
from .choices import Gender


class ScoutSender(BaseModel):
    """
    スカウト送信者モデル

    | カラム名      | カラム名（日本語）  | データ型      | NULL設定   | 外部キー      | ユニークキー |
    |---------------|--------------------|---------------|------------|---------------|--------------|
    | id            | ID                 | int           | NOT NULL   |               |              |
    | company_id    | 企業ID             | int           | NOT NULL   | companies     |              |
    | name          | 名前               | varchar(255)     | NOT NULL   |               |              |
    | department    | 部署               | varchar(255)     | NOT NULL   |               |              |
    | position      | 役職               | varchar(255)     | NOT NULL   |               |              |
    | gender        | 性別               | small_int     | NULL       |               |              |
    | created_at    | 作成日時           | datetime      | NOT NULL   |               |              |
    | updated_at    | 更新日時           | datetime      | NOT NULL   |               |              |
    | deleted_at    | 削除日時           | datetime      | NULL       |               |              |
    """  # noqa: E501, RUF002

    company = models.ForeignKey(
        "Company",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="企業"
    )

    name = models.CharField(
        blank=False,
        null=False,
        max_length=255,
        verbose_name="名前"
    )

    department = models.CharField(
        blank=True,
        null=False,
        max_length=255,
        default="",
        verbose_name="部署"
    )

    position = models.CharField(
        blank=True,
        null=False,
        max_length=255,
        default="",
        verbose_name="役職"
    )

    gender = models.SmallIntegerField(
        blank=False,
        null=False,
        choices=Gender.choices,
        default=Gender.UNSPECIFIED,
        verbose_name="性別"
    )


    class Meta: # noqa: D106
        db_table = "scout_senders"
        verbose_name = verbose_name_plural = "スカウト送信者"
        app_label = "base"

    def __str__(self) -> str: # noqa: D105
        return self.name
