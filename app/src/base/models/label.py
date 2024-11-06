from django.db import models

from .base import BaseModel


class Label(BaseModel):
    """
    ラベルモデル

    | カラム名      | カラム名（日本語）  | データ型      | NULL設定      | 外部キー   | ユニークキー |
    |---------------|--------------------|---------------|---------------|------------|--------------|
    | id            | ID                 | int           | NOT NULL      |            |              |
    | label         | ラベル             | varchar(255)  | NOT NULL      |            | 1            |
    | description   | 説明               | text          | NOT NULL("")  |            |              |
    | is_disabled   | 無効               | boolean       | NOT NULL(0)   |            |              |
    | created_at    | 作成日時           | datetime      | NOT NULL      |            |              |
    | updated_at    | 更新日時           | datetime      | NOT NULL      |            |              |
    | deleted_at    | 削除日時           | datetime      | NULL          |            |              |

    """  # noqa: E501, RUF002

    label = models.CharField(
        blank=False,
        null=False,
        max_length=255,
        unique=True,
        verbose_name="ラベル"
    )

    description = models.TextField(
        blank=True,
        null=False,
        default="",
        verbose_name="説明"
    )

    class Meta:  # noqa: D106
        db_table = "labels"
        verbose_name = verbose_name_plural = "ラベル"
        app_label = "base"

    def __str__(self) -> str:  # noqa: D105
        return self.label
