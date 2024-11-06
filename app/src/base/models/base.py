"""
モデルの基底クラスを定義するモジュール

- BaseModel: モデルの基底クラス。多対多のリレーションを持つモデルに使用する
"""

from django.db import models
from simple_history.models import HistoricalRecords


class BaseModel(models.Model):
    """
    モデルの基底クラス
    """

    created_at = models.DateTimeField(
        blank=True,
        null=False,
        auto_now_add=True,
        editable=False,
        verbose_name="作成日時"
    )

    updated_at = models.DateTimeField(
        blank=True,
        null=False,
        auto_now=True,
        verbose_name="更新日時"
    )

    history = HistoricalRecords(inherit=True, app="base")

    class Meta: # noqa: D106
        abstract = True
        app_label = 'base'
