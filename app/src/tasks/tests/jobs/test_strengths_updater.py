import pytest

from base.models.candidate import Candidate
from base.models.choices import RecruitmentMedia
from base.models.company import Company
from base.models.company_strength import CompanyStrength
from base.models.mail_gen_log import MailGenLog
from base.models.scout import Scout
from base.models.scout_mail import ScoutMail
from tasks.jobs.strengths_updater import StrengthsUpdater
from users.models import CustomUser

baseic_strengths = [
    {
        "strength_id": 1,
        "reason": """"
            候補者はIT技術職としての経験があり、データ分析案件が9割を占める当社の強みは、候補者のスキルと経験を活かせる環境を提供できます。
        """
    },
    {
        "strength_id": 2,
        "reason": """
            候補者はSEとしてシステム開発から運用保守まで幅広い経験があるため、下流～上流まで携わることができる当社の強みは、候補者のキャリア発展に適しています。
        """
    },
    {
        "strength_id": 3,
        "reason": """
            候補者は良い人間関係の職場で働きたいという期待を持っているため、サンドイッチ経営で風通しがよく、年功序列でない当社の強みは、候補者のニーズに合致します。
        """
    }
]
basic_message_body = {
    "mail_gen_log_id": 2,
    "job_type": 5,
    "strengths": baseic_strengths
}


@pytest.fixture
def strengths_updater() -> StrengthsUpdater:
    """Fixture for setting up StrengthsUpdater instance."""
    company = Company.objects.create(id=2)
    CompanyStrength.objects.create(
        id=1, company=company, strength="スキルアップできる"
    )
    CompanyStrength.objects.create(
        id=2, company=company, strength="男女比が5:5"
    )
    CompanyStrength.objects.create(
        id=3, company=company, strength="残業が少ない"
    )
    candidate = Candidate.objects.create(id=1, company=company, company_candidate_id=1)
    scout = Scout.objects.create(
        id=1, candidate=candidate, media=RecruitmentMedia.BIZREACH
    )
    user = CustomUser.objects.create(id=2, email="test@test.com", company=company)
    scout_mail = ScoutMail.objects.create(id=2, scout=scout)
    MailGenLog.objects.create(id=2, scout=scout, user=user, scout_mail=scout_mail)

    return StrengthsUpdater(
        mail_gen_log_id=2,
        message_body=basic_message_body
    )

@pytest.mark.django_db
def test_set_scout_mail_id(strengths_updater: StrengthsUpdater) -> None:
    """Test set_scout_mail_id method."""
    strengths_updater.set_scout_mail_id()

@pytest.mark.django_db
def test_set_company_id(strengths_updater: StrengthsUpdater) -> None:
    """Test set_company_id method."""
    strengths_updater.scout_mail_id=2
    strengths_updater.set_company_id()

@pytest.mark.django_db
def test_set_strengths(strengths_updater: StrengthsUpdater) -> None:
    """Test set_strengths method."""
    strengths_updater.set_strengths()

@pytest.mark.django_db
def test_update(strengths_updater: StrengthsUpdater) -> None:
    """Test update method."""
    strengths_updater.scout_mail_id = 2
    strengths_updater.company_id = 2
    strengths_updater.strengths = baseic_strengths
    strengths_updater.update()
