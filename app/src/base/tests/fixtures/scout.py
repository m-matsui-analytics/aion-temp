import pytest

from base.models import Candidate
from base.models.choices import RecruitmentMedia
from base.models.scout import Scout


# @pytest.mark.django_db(databases=["default"])
# @pytest.mark.django_db
# @pytest.fixture(scope="session")
# @pytest.fixture
def set_base_scout(candidate: Candidate) -> None:
    return Scout.objects.create(
        candidate=candidate,
        media=RecruitmentMedia.BIZREACH
    )
