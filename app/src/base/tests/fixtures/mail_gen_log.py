import pytest

from base.models.mail_gen_log import MailGenLog
from base.models.scout import Scout
from users.models import CustomUser


# @pytest.mark.django_db(databases=["default"])
# @pytest.mark.django_db
# @pytest.fixture(scope="session")
# @pytest.fixture
def set_base_mail_gen_log(scout: Scout, user: CustomUser) -> None:
    """Fixture for setting up MailGenLog instance."""
    return MailGenLog.objects.create(
        scout=scout,
        user=user,
   )

