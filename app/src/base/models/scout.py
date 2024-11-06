from django.core.exceptions import ValidationError
from django.db import models

from .base import BaseModel
from .choices import RecruitmentMedia


class Scout(BaseModel):
    """
    スカウトモデル

    | カラム名                | カラム名（日本語）   | データ型      | NULL設定      | 外部キー              | ユニークキー |
    |-------------------------|----------------------|---------------|-----------  -|-----------------------|--------------|
    | id                      | ID                   | int           | NOT NULL     |                       |              |
    | candidate_id            | 候補者ID             | int           | NOT NULL     | candidates            |              |
    | ideal_candidate_id      | 求める人物像ID       | int           | NULL         | ideal_candidates    |              |
    | matching_rate           | マッチング率         | float         | NULL         |                       |              |
    | is_matched              | マッチング成立       | boolean       | NULL         |                       |              |
    | reason                  | 理由                 | text          | NOT NULL('') |                       |              |
    | media_id                | メディアID           | int           | NOT NULL     | recruitment-medias    |              |
    | send_date               | 送信日               | date          | NULL         |                       |              |
    | send_time               | 送信時間             | time          | NULL         |                       |              |
    | reply_date              | 返信日               | date          | NULL         |                       |              |
    | reply_time              | 返信時間             | time          | NULL         |                       |              |
    | meeting_date            | 面談日               | date          | NULL         |                       |              |
    | meeting_time            | 面談時間             | time          | NULL         |                       |              |
    | created_at              | 作成日時             | datetime      | NOT NULL     |                       |              |
    | updated_at              | 更新日時             | datetime      | NOT NULL     |                       |              |
    | deleted_at              | 削除日時             | datetime      | NULL         |                       |              |

    """  # noqa: E501, RUF002

    candidate = models.OneToOneField(
        "Candidate",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="候補者",
    )

    ideal_candidate = models.ForeignKey(
        "IdealCandidate",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="求める人物像",
    )

    matching_rate = models.FloatField(
        blank=True,
        null=True,
        verbose_name="マッチング率"
    )

    is_matched = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="マッチング成立"
    )

    reason = models.TextField(
        blank=True,
        null=False,
        default="",
        max_length=1000,
        verbose_name="マッチング判定の理由",
    )

    send_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="送信日"
    )

    send_time = models.TimeField(
        blank=True,
        null=True,
        verbose_name="送信時間"
    )

    reply_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="返信日"
    )

    reply_time = models.TimeField(
        blank=True,
        null=True,
        verbose_name="返信時間"
    )

    meeting_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="面談日"
    )

    meeting_time = models.TimeField(
        blank=True,
        null=True,
        verbose_name="面談時間"
    )


    class Meta:  # noqa: D106
        db_table = "scouts"
        verbose_name = verbose_name_plural = "スカウト"
        app_label = "base"

    def __str__(self) -> str:  # noqa: D105
        return self.candidate.id_in_media

    # def clean(self) -> None:
    #     """(必須だけどnull=Trueの場合のみ)必須項目チェック: media"""
    #     if not self.media:
    #         raise ValidationError("Missing required field. [media]")

    # def save(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
    #     """作成・追加時の前処理を追加"""
    #     self.clean()
    #     super().save(*args, **kwargs)
