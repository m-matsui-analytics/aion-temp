from django.db import models
from django.utils import timezone

from .base import BaseModel
from .choices import Plan
from .company_info import CompanyInfo


class Company(BaseModel):
    """
    企業モデル

    | カラム名                | カラム名（日本語） | データ型      | NULL設定    | 外部キー | ユニークキー |
    |-------------------------|--------------------|--------------|------------ |----------|--------------|
    | id                      | ID                 | int          | NOT NULL    |          |              |
    | name                    | 企業名             | varchar(255) | NOT NULL    |          |              |
    | plan                    | プラン             | small_int    | NULL        |          |              |
    | fiscal_year_start_month | 会計年度開始月     | int          | NULL        |          |              |
    | is_tutorial_completed   | チュートリアル完了 | boolean      | NOT NULL(0) |          |              |

    """  # noqa: E501, RUF002

    name = models.CharField(
        blank=False,
        null=False,
        max_length=255,
        verbose_name="企業名"
    )

    plan = models.SmallIntegerField(
        blank=True,
        null=True,
        choices=Plan.choices,
        verbose_name="プラン"
    )

    fiscal_year_start_month = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="会計年度開始月"
    )

    is_tutorial_completed = models.BooleanField(
        blank=True,
        null=False,
        default=False,
        verbose_name="チュートリアル完了"
    )


    class Meta:  # noqa: D106
        db_table = "companies"
        verbose_name = verbose_name_plural = "企業"
        app_label = "base"

    def __str__(self) -> str:  # noqa: D105
        return self.name

    def delete(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003, ARG002
        """論理削除を行い、関連する子モデルも論理削除"""
        now = timezone.now()

        # 論理削除
        self.deleted_at = now
        self.save(update_fields=["deleted_at"])

        # 関連する子モデルの一括論理削除
        related_models = [
            self.candidate_set,
            self.companymedia_set,
            self.idealcandidate_set,
            self.jobposting_set,
            self.kpi_set,
            self.monthlymailcount_set,
            self.recruitmentcontent_set,
            self.scoutsender_set,
            self.strength_set,
            self.customuser_set,
        ]

        # 全ての関連モデルに対して一括更新を実行
        for related_model in related_models:
            related_model.update(deleted_at=now)

        # CompanyInfoの論理削除 (OneToOneFieldなので個別に処理)  # noqa: ERA001
        if hasattr(self, 'companyinfo'):
            CompanyInfo.objects.filter(company=self).update(deleted_at=now)
