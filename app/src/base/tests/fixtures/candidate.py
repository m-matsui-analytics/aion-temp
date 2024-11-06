import pytest

from base.models import Candidate
from base.models.company import Company
from .mail_gen_log import set_base_mail_gen_log
from .scout import set_base_scout
from users.models import CustomUser
# from base.models.

# @pytest.mark.django_db
# @pytest.fixture(scope="session")
# @pytest.fixture
def set_base_candidate(company: Company, user: CustomUser) -> None:
    """Fixture for setting up Candidate instance."""
    for i in range(1, 6):
        candidate =  Candidate.objects.create(
            id=i,
            company=company,
            company_candidate_id=i,
        )
        scout = set_base_scout(candidate)
        set_base_mail_gen_log(scout, user)

