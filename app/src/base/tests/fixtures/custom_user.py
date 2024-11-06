import pytest

from base.models.company import Company
from users.models import CustomUser


# @pytest.mark.django_db(databases=["default"])
# @pytest.mark.django_db
# @pytest.fixture(scope="session")
# @pytest.fixture
def setup_base_custom_user(company: Company):
    """Set up CustomUser data."""
    return CustomUser.objects.create(
        id=1,
        email="test@test.com",
        password="Testtest111",
        account_status=CustomUser.AccountStatus.ACTIVE,
        company=company,
    )
