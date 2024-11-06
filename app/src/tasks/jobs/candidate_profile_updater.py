from django.utils import timezone

from base.models.candidate import Candidate
from base.models.candidate_feeling import CandidateFeeling
from base.models.work_value import WorkValue
from tasks.exceptions import DBError


class CandidateProfileUpdater:
    """
    候補者のプロフィール情報を更新する

    Args:
        candidate_id (int): 候補者ID
        candidate_profile (dict): 候補者プロフィールデータ

    """

    def __init__(self, candidate_id: int, candidate_profile: dict) -> None:  # noqa: D107
        self.candidate_id = candidate_id
        self.candidate_profile = candidate_profile

    def update(self) -> None:  # noqa: PLR0912
        """
        候補者のプロフィール情報を更新する
        """
        try:
            work_value_1_id = self.candidate_profile.get("work_value_1")
            if not work_value_1_id:
                work_value_1 = None
            else:
                work_value_1 = WorkValue.objects.get(pk=work_value_1_id)

            work_value_2_id = self.candidate_profile.get("work_value_2")
            if not work_value_2_id:
                work_value_2 = None
            else:
                work_value_2 = WorkValue.objects.get(pk=work_value_2_id)

            expectation_1_id = self.candidate_profile.get("expectation_1")
            if not expectation_1_id:
                expectation_1 = None
            else:
                expectation_1 = CandidateFeeling.objects.get(pk=expectation_1_id)

            expectation_2_id = self.candidate_profile.get("expectation_2")
            if not expectation_2_id:
                expectation_2 = None
            else:
                expectation_2 = CandidateFeeling.objects.get(pk=expectation_2_id)

            dissatisfaction_1_id = self.candidate_profile.get("dissatisfaction_1")
            if not dissatisfaction_1_id:
                dissatisfaction_1 = None
            else:
                dissatisfaction_1 = CandidateFeeling.objects.get(pk=dissatisfaction_1_id)

            dissatisfaction_2_id = self.candidate_profile.get("dissatisfaction_2")
            if not dissatisfaction_2_id:
                dissatisfaction_2 = None
            else:
                dissatisfaction_2 = CandidateFeeling.objects.get(pk=dissatisfaction_2_id)

            anxiety_1_id = self.candidate_profile.get("anxiety_1")
            if not anxiety_1_id:
                anxiety_1 = None
            else:
                anxiety_1 = CandidateFeeling.objects.get(pk=anxiety_1_id)

            anxiety_2_id = self.candidate_profile.get("anxiety_2")
            if not anxiety_2_id:
                anxiety_2 = None
            else:
                anxiety_2 = CandidateFeeling.objects.get(pk=anxiety_2_id)

            Candidate.objects.filter(pk=self.candidate_id).update(
                last_name=self.candidate_profile.get("last_name") or "",
                first_name=self.candidate_profile.get("first_name") or "",
                gender=self.candidate_profile.get("gender"),
                age=self.candidate_profile.get("age"),
                prefecture=self.candidate_profile.get("prefecture"),
                industry=self.candidate_profile.get("industry"),
                occupation=self.candidate_profile.get("occupation"),
                position=self.candidate_profile.get("position"),
                current_company=self.candidate_profile.get("current_company", ""),
                department=self.candidate_profile.get("department", ""),
                job_title=self.candidate_profile.get("job_title") or "",
                current_annual_income_min=self.candidate_profile.get("current_annual_income_min"),
                current_annual_income_max=self.candidate_profile.get("current_annual_income_max"),
                work_value_1=work_value_1,
                work_value_2=work_value_2,
                expectation_1=expectation_1,
                expectation_2=expectation_2,
                dissatisfaction_1=dissatisfaction_1,
                dissatisfaction_2=dissatisfaction_2,
                anxiety_1=anxiety_1,
                anxiety_2=anxiety_2,
                is_career_change=self.candidate_profile.get("is_career_change"),
                preferred_annual_income=self.candidate_profile.get("preferred_annual_income"),
                updated_at=timezone.now()
            )

        except Exception as e:
            error_msg = f"<{__name__}> DBError: {e}"
            raise DBError(error_msg) from e
