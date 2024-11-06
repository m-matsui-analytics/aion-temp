import pytest

from base.models.candidate import Candidate
from base.models.choices import RecruitmentMedia
from base.models.company import Company
from base.models.mail_gen_log import MailGenLog
from base.models.scout import Scout
from base.models.scout_mail import ScoutMail
from tasks.jobs.gen_mail_option_updater import GenMailOptionUpdater
from users.models import CustomUser


@pytest.fixture
def gen_mail_option_updater() -> GenMailOptionUpdater:
    """Fixture for setting up GenMailOptionUpdater instance."""

    company = Company.objects.create(id=2)
    candidate = Candidate.objects.create(id=1, company=company, company_candidate_id=1)
    scout = Scout.objects.create(id=1, candidate=candidate, media=RecruitmentMedia.BIZREACH)
    print("scout: " + str(scout))
    user = CustomUser.objects.create(id=2, email="test@test.com", company=company)
    scout_mail = ScoutMail.objects.create(id=2, scout=scout)
    MailGenLog.objects.create(id=2, scout=scout, user=user, scout_mail=scout_mail)

    return GenMailOptionUpdater(
        mail_gen_log_id=2,
        message_body={
            "empathy_emotion": 1,
            "mail_structure": 1
        }
    )

@pytest.mark.django_db
def test_set_scout_mail_id(gen_mail_option_updater: GenMailOptionUpdater) -> None:
    """Test set_scout_mail_id method."""
    gen_mail_option_updater.set_scout_mail_id()

@pytest.mark.django_db
def test_set_empathy_emotion(gen_mail_option_updater: GenMailOptionUpdater) -> None:
    """Test set_empathy_emotion method."""
    gen_mail_option_updater.set_empathy_emotion()

@pytest.mark.django_db
def test_set_mail_structure(gen_mail_option_updater: GenMailOptionUpdater) -> None:
    """Test set_mail_structure method."""
    gen_mail_option_updater.set_mail_structure()

@pytest.mark.django_db
def test_update(gen_mail_option_updater: GenMailOptionUpdater) -> None:
    """Test update method."""
    gen_mail_option_updater.scout_mail_id = 2
    gen_mail_option_updater.empathy_emotion = 1
    gen_mail_option_updater.mail_structure = 3
    gen_mail_option_updater.update()
