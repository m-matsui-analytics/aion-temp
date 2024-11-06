from typing import Any

from factory import Faker
from factory.django import DjangoModelFactory

from base.models import WorkValue


class WorkValueFactory(DjangoModelFactory):
    """
    WorkValueFactory
    """

    class Meta:  # noqa: D106
        model = WorkValue

    # ランダムな文字列を生成
    work_value = Faker("text")
    description = Faker("text")

    @classmethod
    def _create(
        cls,
        model_class: type[WorkValue],
        *args: tuple[Any],  # noqa: ARG003
        **kwargs: Any  # noqa: ANN401
    ) -> WorkValue:
        """
        Override the default _create method to use get_or_create
        """
        obj, created = model_class.objects.get_or_create(**kwargs)
        return obj
