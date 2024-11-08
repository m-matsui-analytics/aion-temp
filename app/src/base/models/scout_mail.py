from django.db import models

from .base import BaseModel
from .choices import (
    EmpathyEmotion,
    MailGenStatus,
    MailStructureType,
)


class ScoutMail(BaseModel):
    """
    スカウトメールモデル

    | カラム名               | カラム名(日本語)   | データ型   | NULL設定       | 外部キー       | ユニークキー |
    |------------------------|--------------------|------------|----------------|----------------|--------------|
    | id                     | ID                 | int        | NOT NULL       |                |              |
    | scout_id               | スカウトID         | int        | NOT NULL       | scouts         | 1            |
    | subject                | 件名               | char(250)  | NOT NULL('')   |                |              |
    | body                   | 本文               | text       | NOT NULL('')   |                |              |
    | empathy_emotion        | 共感する感情       | small_int  | NULL           |                |              |
    | mail_structure         | メール構成         | small_int  | NULL           |                |              |
    | strength_1             | 強み1              | int        | NULL           | strengths      |              |
    | strength_2             | 強み2              | int        | NULL           | strengths      |              |
    | strength_3             | 強み3              | int        | NULL           | strengths      |              |
    | job-posting_id         | 求人票ID           | int        | NULL           | job-postings   |              |
    | recruitment_article_1  | 採用記事1        | int        | NULL           | recruitment_articles       |              |
    | recruitment_article_2  | 採用記事2        | int        | NULL           | recruitment_articles       |              |
    | recruitment_article_3  | 採用記事3        | int        | NULL           | recruitment_articles       |              |
    | gen_status             | 作成状況           | small_int  | NULL           |                |              |
    | scout_sender           | スカウト送信者     | int        | NULL           | scout_senders  |              |
    | created_at             | 作成日時           | datetime   | NOT NULL       |                |              |
    | updated_at             | 更新日時           | datetime   | NOT NULL       |                |              |
    | deleted_at             | 削除日時           | datetime   | NULL           |                |              |
    """  # noqa: E501

    scout = models.ForeignKey(
        "Scout",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="スカウト",
    )

    subject = models.CharField(
        blank=False,
        null=False,
        default="",
        max_length=250,
        verbose_name="件名",
    )

    body = models.TextField(
        blank=False,
        null=False,
        default="",
        verbose_name="本文",
    )

    empathy_emotion = models.SmallIntegerField(
        blank=True,
        null=True,
        choices=EmpathyEmotion.choices,
        verbose_name="共感する感情",
    )

    mail_structure = models.SmallIntegerField(
        blank=True,
        null=True,
        choices=MailStructureType.choices,
        verbose_name="メール構成",
    )

    strength_1 = models.ForeignKey(
        "CompanyStrength",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="strength_1",
        verbose_name="強み1",
    )

    strength_2 = models.ForeignKey(
        "CompanyStrength",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="strength_2",
        verbose_name="強み2",
    )

    strength_3 = models.ForeignKey(
        "CompanyStrength",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="strength_3",
        verbose_name="強み3",
    )

    job_posting = models.ForeignKey(
        "JobPosting",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="求人票",
    )

    recruitment_article_1 = models.ForeignKey(
        "RecruitmentArticle",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="recruitment_article_1",
        verbose_name="採用記事1",
    )

    recruitment_article_2 = models.ForeignKey(
        "RecruitmentArticle",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="recruitment_article_2",
        verbose_name="採用記事2",
    )

    recruitment_article_3 = models.ForeignKey(
        "RecruitmentArticle",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="採用記事3",
    )

    gen_status = models.SmallIntegerField(
        blank=True,
        null=True,
        choices=MailGenStatus.choices,
        verbose_name="作成状況",
    )

    scout_sender = models.ForeignKey(
        "ScoutSender",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="差出人",
    )

    scout_sender_reason = models.TextField(
        blank=True,
        null=False,
        default="",
        verbose_name="差出人の選択理由",
    )

    is_checked = models.BooleanField(
        blank=False,
        null=False,
        default=False,
        verbose_name="確認済み",
    )


    class Meta:  # noqa: D106
        db_table = "scout_mails"
        verbose_name = verbose_name_plural = "スカウトメール"
        app_label = "base"

    def __str__(self) -> str:  # noqa: D105
        return self.subject
