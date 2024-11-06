"""
base.modelsのすべてを一括でexportするためのファイル
"""

from .base import BaseModel  # noqa: F401
from .candidate import Candidate, HistoricalCandidate  # noqa: F401
from .candidate_academic_history import CandidateAcademicHistory  # noqa: F401
from .candidate_certification import CandidateCertification  # noqa: F401
from .candidate_feeling import CandidateFeeling  # noqa: F401
from .candidate_label import CandidateLabel  # noqa: F401
from .candidate_preferred_industry import CandidatePreferredIndustry  # noqa: F401
from .candidate_preferred_location import CandidatePreferredLocation  # noqa: F401
from .candidate_preferred_occupation import CandidatePreferredOccupation  # noqa: F401
from .candidate_skill import CandidateSkill  # noqa: F401
from .candidate_work_history import CandidateWorkHistory  # noqa: F401
from .choices import (
    Education,  # noqa: F401
    EmpathyEmotion,  # noqa: F401
    EmployeeSize,  # noqa: F401
    EmploymentStatus,  # noqa: F401
    Gender,  # noqa: F401
    HTMLContentAnalysisErrorType,  # noqa: F401
    HTMLContentAnalysisProcess,  # noqa: F401
    HTMLContentAnalysisStatus,  # noqa: F401
    Industry,  # noqa: F401
    MailGenErrorType,  # noqa: F401
    MailGenProcess,  # noqa: F401
    MailGenStatus,  # noqa: F401
    MailStructureType,  # noqa: F401
    Occupation,  # noqa: F401
    Plan,  # noqa: F401
    Position,  # noqa: F401
    Prefecture,  # noqa: F401
    RangeType,  # noqa: F401
    RecruitmentMedia,  # noqa: F401
    RequirementCategory,  # noqa: F401
    RequirementLevel,  # noqa: F401
)
from .company import Company  # noqa: F401
from .company_info import CompanyInfo  # noqa: F401
from .company_media import CompanyMedia  # noqa: F401
from .company_strength import CompanyStrength  # noqa: F401
from .company_strength_jp import CompanyStrengthJP  # noqa: F401
from .company_strength_ra import CompanyStrengthRA  # noqa: F401
from .ideal_candidate import IdealCandidate  # noqa: F401
from .ideal_candidate_jp import IdealCandidateJP  # noqa: F401
from .ideal_candidate_ra import IdealCandidateRA  # noqa: F401
from .ideal_candidate_requirement import IdealCandidateRequirement  # noqa: F401
from .job_posting import JobPosting  # noqa: F401
from .job_posting_analysis_log import JobPostingAnalysisLog  # noqa: F401
from .kpi import KPI  # noqa: F401
from .label import Label  # noqa: F401
from .mail_gen_log import MailGenLog  # noqa: F401
from .monthly_mail_count import MonthlyMailCount  # noqa: F401
from .recruitment_article import RecruitmentArticle  # noqa: F401
from .recruitment_article_analysis_log import (
    RecruitmentArticleAnalysisLog,  # noqa: F401
)
from .scout import Scout  # noqa: F401
from .scout_mail import ScoutMail  # noqa: F401
from .scout_sender import ScoutSender  # noqa: F401
from .work_value import WorkValue  # noqa: F401

