from django.db import models

from .base import BaseModel


class WorkValue(BaseModel):
    """
    仕事観モデル

    | カラム名      | カラム名（日本語）  | データ型      | NULL設定      | 外部キー   | ユニークキー |
    |---------------|--------------------|---------------|---------------|------------|--------------|
    | id            | ID                 | int           | NOT NULL      |            |              |
    | work_value    | 仕事観             | varchar(255)  | NOT NULL      |            | 1            |
    | description   | 説明               | text          | NOT NULL("")  |            |              |
    | is_disabled   | 無効               | boolean       | NOT NULL(0)   |            |              |
    | created_at    | 作成日時           | datetime      | NOT NULL      |            |              |
    | updated_at    | 更新日時           | datetime      | NOT NULL      |            |              |
    | deleted_at    | 削除日時           | datetime      | NULL          |            |              |

    """  # noqa: E501, RUF002

    work_value = models.CharField(
        blank=False,
        null=False,
        max_length=255,
        unique=True,
        verbose_name="仕事観"
    )

    description = models.TextField(
        blank=True,
        null=False,
        default="",
        verbose_name="説明"
    )

    is_disabled = models.BooleanField(
        blank=False,
        null=False,
        default=False,
        verbose_name="無効"
    )


    class Meta:  # noqa: D106
        db_table = "work_values"
        verbose_name = verbose_name_plural = "仕事観"
        app_label = "base"

    def __str__(self) -> str:  # noqa: D105
        return self.work_value
