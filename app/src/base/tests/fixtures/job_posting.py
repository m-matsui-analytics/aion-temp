import pytest

from base.models.choices import RecruitmentMedia
from base.models.company import Company
from base.models.job_posting import JobPosting
from base.models.job_posting_analysis_log import JobPostingAnalysisLog


# @pytest.mark.django_db(databases=["default"])
# @pytest.mark.django_db
# @pytest.fixture(scope="session")
# @pytest.fixture
def set_base_job_posting(company: Company, user) -> None:
    """Set job_posting data."""

    for i in range(1, 6):
        jp = JobPosting.objects.create(
            id=i,
            company=company,
            title="test_job",
            url=f"http://test.com/testtest/{i}/",
            media=RecruitmentMedia.BIZREACH,
        )
        JobPostingAnalysisLog.objects.create(
            job_posting=jp,
            user=user,
        )
