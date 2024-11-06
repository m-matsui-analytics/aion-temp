from django.db import models

from .base import BaseModel
from .choices import HTMLContentAnalysisErrorType, HTMLContentAnalysisProcess


class RecruitmentArticleAnalysisLog(BaseModel):
    """
    コンテンツ解析ログモデル

    | No  | カラム名           | カラム名（日本語） | データ型     | NULL設定      | 外部キー       | ユニークキー | プログラミング定数                |
    | --- | ------------------ | ------------------ | ------------ | ------------- | -------------- | ----------- | ---------------------------------- |
    | 1   | id                 | ID                 | int          | NOT NULL      |                |             |                                    |
    | 2   | recruitment_article_id         | 記事ID       | int          | NOT NULL      | job-postings   |             |                                    |
    | 3   | user_id            | 登録者ID           | int          | NOT NULL      | users          |             |                                    |
    | 4   | is_notified        | 通知済みフラグ     | boolean      | NOT NULL(0)   |                |             |                                    |
    | 5   | is_reanalysis       | 再作成フラグ       | boolean      | NOT NULL(0)   |                |             |                                    |
    | 6   | start_process      | 開始プロセス       | int          | NULL          |                |             | HTMLContentAnalysisProcess         |
    | 7   | error_process      | エラープロセス     | int          | NULL          |                |             | HTMLContentAnalysisProcess         |
    | 8   | error_type         | エラータイプ       | small_int    | NULL          |                |             | HTMLContentAnalysisErrorType       |
    | 9   | created_at         | 作成日時           | datetime     | NOT NULL      |                |             |                                    |
    | 10  | updated_at         | 更新日時           | datetime     | NOT NULL      |                |             |                                    |

    """  # noqa: E501, RUF002

    recruitment_article = models.ForeignKey(
        "RecruitmentArticle",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="採用記事",
    )

    user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="登録者",
    )

    is_reanalysis = models.BooleanField(
        blank=False,
        null=False,
        default=False,
        verbose_name="再作成",
    )

    start_process = models.SmallIntegerField(
        blank=True,
        null=True,
        choices=HTMLContentAnalysisProcess.choices,
        default=HTMLContentAnalysisProcess.FETCH_HTML,
        verbose_name="開始プロセス",
    )

    error_process = models.SmallIntegerField(
        blank=True,
        null=True,
        choices=HTMLContentAnalysisProcess.choices,
        verbose_name="エラープロセス",
    )

    error_type = models.SmallIntegerField(
        blank=True,
        null=True,
        choices=HTMLContentAnalysisErrorType.choices,
        verbose_name="エラータイプ",
    )

    is_notified = models.BooleanField(
        blank=False,
        null=False,
        default=False,
        verbose_name="通知済",
    )

    class Meta:  # noqa: D106
        db_table = "recruitment_article_analysis_logs"
        verbose_name = verbose_name_plural = "採用記事解析ログ"
        app_label = "base"

    def __str__(self) -> str:  # noqa: D105
        return str(self.recruitment_article.id)

    def save(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """作成・追加時の前処理を追加"""
        self.clean()
        super().save(*args, **kwargs)
