"""
Views for the API
"""

from .candidate import CandidateView  # noqa: F401
from .company_info import (
    # CompanyInfoRetrieveView,
    # CompanyInfoUpdateView,
    CompanyInfoView,  # noqa: F401
)
from .company_media import CompanyMediaView  # noqa: F401
from .empathy_emotion import EmpathyEmotionView  # noqa: F401
from .employee_size import EmployeeSizeView  # noqa: F401
from .gender import GenderView  # noqa: F401
from .ideal_candidate import IdealCandidateListView  # noqa: F401
from .industry import IndustryView  # noqa: F401
from .job_posting import (
    JobPostingCreateTextView,  # noqa: F401
    JobPostingCreateURLView,  # noqa: F401
    JobPostingView,  # noqa: F401
)
from .mail_gen_error_type import MailGenErrorTypeView  # noqa: F401
from .mail_gen_status import MailGenStatusView  # noqa: F401
from .mail_structure_type import MailStructureTypeView  # noqa: F401
from .occupation import OccupationView  # noqa: F401
from .plan import PlanView  # noqa: F401
from .position import PositionView  # noqa: F401
from .prefecture import PrefectureView  # noqa: F401
from .recruitment_article import (
    RecruitmentArticleCreateTextView,  # noqa: F401
    RecruitmentArticleCreateURLView,  # noqa: F401
    RecruitmentArticleView,  # noqa: F401
)
from .recruitment_media import RecruitmentMediaView  # noqa: F401
from .requirement_level import RequirementLevelView  # noqa: F401
from .user import (
    CustomTokenObtainPairView,  # noqa: F401
    CustomTokenRefreshView,  # noqa: F401
    CustomTokenVerifyView,  # noqa: F401
    UserView,  # noqa: F401
)
