from django.db import models

from .base import BaseModel
from .choices import EmpathyEmotion


class CandidateFeeling(BaseModel):
    """
    転職に対する気持ちモデル

    | カラム名      | カラム名（日本語） | データ型      | NULL設定      | 外部キー   | ユニークキー |
    |---------------|--------------------|--------------|---------------|------------|--------------|
    | id            | ID                 | int          | NOT NULL      |            |              |
    | emotion_type  | 感情タイプ         | small_int    | NOT NULL      |            |              |
    | feeling          | 転職に対する気持ち | varchar(255) | NOT NULL      |            | 1            |
    | description   | 説明               | text         | NOT NULL('')  |            |              |
    | is_disabled   | 無効               | boolean      | NOT NULL(0)   |            |              |
    | created_at    | 作成日時           | datetime     | NOT NULL      |            |              |
    | updated_at    | 更新日時           | datetime     | NOT NULL      |            |              |

    """  # noqa: E501, RUF002

    emotion_type = models.SmallIntegerField(
        blank=False,
        null=False,
        choices=EmpathyEmotion.choices,
        verbose_name="感情タイプ"
    )

    feeling = models.CharField(
        blank=False,
        null=False,
        max_length=255,
        verbose_name="転職に対する気持ち",
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
        db_table = "candidate_feelings"
        verbose_name = verbose_name_plural = "転職に対する気持ち"
        app_label = 'base'

    def __str__(self) -> str:  # noqa: D105
        return self.feeling

