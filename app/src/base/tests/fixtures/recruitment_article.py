import pytest

from base.models.choices import RecruitmentMedia
from base.models.company import Company
from base.models.recruitment_article import RecruitmentArticle
from base.models.recruitment_article_analysis_log import RecruitmentArticleAnalysisLog
from users.models import CustomUser


# @pytest.mark.django_db(databases=["default"])
# @pytest.mark.django_db
# @pytest.fixture(scope="session")
# @pytest.fixture
def set_base_recruitment_article(company: Company, user: CustomUser) -> None:
    """Set up CustomUser data."""
    for i in range(1, 6):
        ra = RecruitmentArticle.objects.create(
            id=i,
            company=company,
            title="test_recruitment_article",
            url=f"http://test.com/testtest/{i}/",
            media=RecruitmentMedia.BIZREACH,
        )
        RecruitmentArticleAnalysisLog.objects.create(
            recruitment_article=ra,
            user=user,
        )
