import pytest

from .company import set_base_company
from .company_info import set_base_company_info
from .company_strength import set_base_company_strengths
from .custom_user import setup_base_custom_user
from .ideal_candidate import set_base_ideal_candidate
from .job_posting import set_base_job_posting
from .recruitment_article import set_base_recruitment_article
from .scout_sender import set_base_scout_sender
from .candidate import set_base_candidate


@pytest.fixture
# @pytest.mark.django_db
def set_base_data() -> None:
    """Set base data."""
    company = set_base_company()
    user = setup_base_custom_user(company)
    set_base_company_info(company)
    set_base_company_strengths(company)
    set_base_ideal_candidate(company)
    set_base_job_posting(company, user)
    set_base_recruitment_article(company, user)
    set_base_scout_sender(company)
    set_base_candidate(company, user)

    return company
