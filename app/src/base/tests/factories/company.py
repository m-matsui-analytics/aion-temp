from typing import Any

import factory
from factory import Faker

from base.models import Company, Plan


class CompanyFactory(factory.django.DjangoModelFactory):
    """
    CompanyFactory
    """

    class Meta:  # noqa: D106
        model = Company

    name = Faker("company")  # 企業名としてFakerの会社名を利用
    plan = factory.Iterator([choice[0] for choice in Plan.choices])  # Planのchoicesからランダムに選択
    fiscal_year_start_month = factory.Faker('random_int', min=1, max=12)  # 1月〜12月の範囲でランダムな整数
    is_tutorial_completed = factory.Faker('boolean')  # True/Falseをランダムに生成

    @classmethod
    def _create(
        cls,
        model_class: type[Company],
        *args: tuple[Any],  # noqa: ARG003
        **kwargs: Any  # noqa: ANN401
    ) -> Company:
        """
        Override the default _create method to use get_or_create
        """
        # id と name で既存データを検索するように修正
        lookup_fields = {key: kwargs.pop(key) for key in ['id', 'name'] if key in kwargs}

        # 残りの kwargs は defaults に渡す
        obj, created = model_class.objects.get_or_create(defaults=kwargs, **lookup_fields)
        return obj
