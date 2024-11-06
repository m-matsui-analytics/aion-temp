# your_app/signals.py
from typing import Any

from django.db.models import Model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Company, CompanyInfo


@receiver(post_save, sender=Company)
def create_company_info(
        sender: type[Model],  # noqa: ARG001
        instance: Company,
         *,
        created: bool,
        **kwargs: dict[str, Any]  # noqa: ARG001
    ) -> None:
    """
    企業が追加されたら、会社情報も同時に作成する。
    """
    if created:
        # CompanyInfoが存在しない場合のみ作成
        CompanyInfo.objects.create(company=instance)
