
from typing import Any

import factory
from factory import Faker
from factory.django import DjangoModelFactory

from base.models import (
    Education,
    EmploymentStatus,
    IdealCandidate,
    Industry,
    Occupation,
    RangeType,
)
from base.tests.factories.company import CompanyFactory


class IdealCandidateFactory(DjangoModelFactory):
    """
    IdealCandidate Factory
    """

    class Meta:
        model = IdealCandidate


    # 企業ID = 1の企業を紐づける
    company = CompanyFactory(id=1)
    # company = factory.SubFactory('base.tests.factories.company.CompanyFactory')  # CompanyFactoryを使って関連データを生成
    name = Faker('name')  # 人物像名としてFakerの名前を利用
    age_min = Faker('random_int', min=20, max=30)  # 年齢（下限）をランダムに生成
    age_max = Faker('random_int', min=31, max=60)  # 年齢（上限）をランダムに生成
    education = factory.Iterator([choice[0] for choice in Education.choices])  # 学歴の選択肢からランダムに選択
    preferred_industry = factory.Iterator([choice[0] for choice in Industry.choices])  # 希望業界の選択肢からランダムに選択
    preferred_occupation = factory.Iterator([choice[0] for choice in Occupation.choices])  # 希望職種の選択肢からランダムに選択
    current_position = factory.Iterator([choice[0] for choice in Occupation.choices])  # 現在の役職の選択肢からランダムに選択
    current_annual_income = Faker('random_int', min=300, max=1500)  # 年収をランダムに生成
    income_range_type = factory.Iterator([choice[0] for choice in RangeType.choices])  # 年収の範囲をランダムに選択
    employment_status = factory.Iterator([choice[0] for choice in EmploymentStatus.choices])  # 就業状況をランダムに選択
    work_value_1 = factory.SubFactory('base.tests.factories.work_value.WorkValueFactory')  # WorkValueFactoryを使って関連データを生成
    work_value_2 = factory.SubFactory('base.tests.factories.work_value.WorkValueFactory')  # WorkValueFactoryを使って関連データを生成
    work_value_3 = factory.SubFactory('base.tests.factories.work_value.WorkValueFactory')  # WorkValueFactoryを使って関連データを生成

    @classmethod
    def _create(
        cls,
        model_class: type[IdealCandidate],
        *args: tuple[Any],  # noqa: ARG003
        **kwargs: Any  # noqa: ANN401
    ) -> IdealCandidate:
        """
        Override the default _create method to use get_or_create
        """
        obj, created = model_class.objects.get_or_create(**kwargs)
        return obj
