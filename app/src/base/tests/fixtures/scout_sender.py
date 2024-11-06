import pytest

from base.models.choices import Gender, Position
from base.models.company import Company
from base.models.scout_sender import ScoutSender


# @pytest.mark.django_db(databases=["default"])
# @pytest.mark.django_db
# @pytest.fixture(scope="session")
# @pytest.fixture
def set_base_scout_sender(company: Company) -> None:
    ScoutSender.objects.create(
        company=company,
        name="test_name",
        department="test_department",
        position=Position.PRESIDENT,
        gender=Gender.FEMALE
    )
    ScoutSender.objects.create(
        company=company,
        name="test_name",
        department="test_department",
        position=Position.SECTION_MANAGER,
        gender=Gender.MALE,
    )
