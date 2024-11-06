
from django.contrib import admin

from base.admin.base import BaseAdmin
from base.models import Candidate


class CandidateAdmin(BaseAdmin):
    """
    (管理画面設定) 候補者
    """

    # list_display: ClassVar = [
    #     "company_id",
    #     "company_candidate_id",
    #     "current_company",
    # ]



admin.site.register(Candidate, CandidateAdmin)
