from django.core.exceptions import ValidationError
from django.db import models

from .base import BaseModel
from .choices import MailGenErrorType, MailGenProcess


class MailGenLog(BaseModel):
    """
    メール作成ログモデル

    | カラム名          | カラム名（日本語）     | データ型      | NULL設定     | 外部キー   | ユニークキー |
    |-------------------|-----------------------|---------------|--------------|------------|--------------|
    | id                | ID                    | int           | NOT NULL     |            |              |
    | scout_id          | スカウトID            | int           | NOT NULL     | scouts     |              |
    | user_id           | 作成者ID              | int           | NOT NULL     | users      |              |
    | is_notified       | 通知済                | boolean       | NOT NULL(0)  |            |              |
    | is_regeneration   | 再作成                | boolean       | NOT NULL(0)  |            |              |
    | error_type        | エラータイプ          | small_int     | NULL         |            |              |
    | error_point       | エラー発生箇所        | char(250)     | NOT NULL('') |            |              |
    | created_at        | 作成日時              | datetime      | NOT NULL     |            |              |
    | updated_at        | 更新日時              | datetime      | NOT NULL     |            |              |
    | deleted_at        | 削除日時              | datetime      | NULL         |            |              |
    """  # noqa: E501, RUF002

    scout = models.ForeignKey(
        "Scout",
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="スカウト",
    )

    scout_mail = models.OneToOneField(
        "ScoutMail",
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="スカウトメール",
    )
    user = models.ForeignKey(
        "users.CustomUser",
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="作成者",
    )

    is_notified = models.BooleanField(
        blank=False,
        null=False,
        default=False,
        verbose_name="通知済",
    )

    start_process = models.SmallIntegerField(
        blank=True,
        null=True,
        choices=MailGenProcess.choices,
        default=MailGenProcess.EXTRACT_CANDIDATE_PROFILE,
        verbose_name="開始プロセス",
    )

    error_process = models.SmallIntegerField(
        blank=True,
        null=True,
        choices=MailGenProcess.choices,
        verbose_name="エラープロセス",
    )

    error_type = models.SmallIntegerField(
        blank=True,
        null=True,
        choices=MailGenErrorType.choices,
        verbose_name="エラータイプ",
    )

    class Meta:  # noqa: D106
        db_table = "mail_gen_logs"
        verbose_name = verbose_name_plural = "メール作成ログ"
        app_label = "base"

    def __str__(self) -> str:  # noqa: D105
        return str(self.scout.candidate.id)

    def clean(self) -> None:
        """(必須だけどnull=Trueの場合のみ)必須項目チェック: scout"""
        if not self.scout:
            raise ValidationError("Missing required field. [scout]")
        """(必須だけどnull=Trueの場合のみ)必須項目チェック: user"""
        if not self.user:
            raise ValidationError("Missing required field. [user]")

    def save(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """作成・追加時の前処理を追加"""
        self.clean()
        super().save(*args, **kwargs)
