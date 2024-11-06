"""
Serializers for the API.
"""

from .candidate import CandidateSerializer  # noqa: F401
from .company_info import CompanyInfoSerializer  # noqa: F401
from .company_media import (  # noqa: F401
    CompanyMediaDeleteSerializer,
    CompanyMediaSerializer,
)
from .error import ErrorResponseSerializer  # noqa: F401
from .ideal_candidate import (
    IdealCandidateSerializer,  # noqa: F401
)
from .job_posting import (
    JobPostingCreateTextSerializer,  # noqa: F401
    JobPostingCreateURLSerializer,  # noqa: F401
    JobPostingListSerializer,  # noqa: F401
    JobPostingSerializer,  # noqa: F401
)
from .recruitment_article import (
    RecruitmentArticleCreateTextSerializer,  # noqa: F401
    RecruitmentArticleCreateURLSerializer,  # noqa: F401
    RecruitmentArticleListSerializer,  # noqa: F401
    RecruitmentArticleSerializer,  # noqa: F401
)
from .user import (
    CustomTokenObtainPairSerializer,  # noqa: F401
    CustomTokenRefreshSerializer,  # noqa: F401
    CustomTokenVerifySerializer,  # noqa: F401
    UserSerializer,  # noqa: F401
)
