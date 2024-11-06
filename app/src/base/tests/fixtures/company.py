import pytest

from base.models.choices import Plan
from base.models.company import Company


# @pytest.mark.django_db
def set_base_company():
    return Company.objects.create(
        id=2,
        name="test_company",
        plan=Plan.PREMIUM
    )
