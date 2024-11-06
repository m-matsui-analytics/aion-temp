import pytest
from django.core.management import call_command

from base.tests.fixtures.candidate import set_base_candidate
from base.tests.fixtures.company import set_base_company
from base.tests.fixtures.company_info import set_base_company_info
from base.tests.fixtures.company_strength import set_base_company_strengths
from base.tests.fixtures.custom_user import setup_base_custom_user
from base.tests.fixtures.ideal_candidate import set_base_ideal_candidate
from base.tests.fixtures.job_posting import set_base_job_posting
from base.tests.fixtures.recruitment_article import set_base_recruitment_article
from base.tests.fixtures.scout_sender import set_base_scout_sender


# テスト前にデータベースをリセット
@pytest.fixture(autouse=True)
# @pytest.fixture(autouse=True, scope="function")
def reset_db():
    call_command("flush", "--noinput")


@pytest.fixture(autouse=True)
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
