import logging

from django.db import transaction
from django.utils import timezone

from base.models.candidate_academic_history import CandidateAcademicHistory
from base.models.candidate_certification import CandidateCertification
from base.models.candidate_skill import CandidateSkill
from base.models.candidate_work_history import CandidateWorkHistory
from tasks.exceptions import DBError


# def update_caree
class CareerDetailUpdater:
    """
    候補者のキャリア詳細情報を更新する

    Args:
        candidate_id (int): 候補者ID
        career_detail (dict): 候補者のキャリア詳細情報

    """

    def __init__(self, candidate_id: int, career_detail: dict) -> None:
        self.candidate_id = candidate_id
        self.career_detail = career_detail

    @transaction.atomic
    def update(self) -> None:
        """
        候補者のキャリア詳細情報を更新する
        """
        try:
            if self.career_detail.get("academic_history"):
                self.updae_candidate_academic_history()

            if self.career_detail.get("work_history"):
                self.update_candidate_work_history()

            if self.career_detail.get("certifications"):
                self.update_candidate_certifications()

            if self.career_detail.get("skills"):
                self.update_candidate_skills()
        except DBError as e:
            error_msg = f"<{__name__}> DBError: {e}"
            print(error_msg)
            raise DBError(error_msg) from e


    def updae_candidate_academic_history(self) -> None:
        """
        候補者の学歴を登録する
        """
        print("updae_candidate_academic_history")
        # 既存の学歴情報を削除
        old_academic_history = CandidateAcademicHistory.objects.filter(
            candidate_id=self.candidate_id
        )

        for academic_history in old_academic_history:
            print("delete academic_history")
            academic_history.delete()

        # 新しい学歴情報を登録
        for academic_history in self.career_detail["academic_history"]:
            try:
                CandidateAcademicHistory.objects.create(
                    candidate_id=self.candidate_id,
                    enrollment_date=academic_history.get("enrollment_date"),
                    graduation_date=academic_history.get("graduation_date"),
                    school=academic_history.get("school"),
                    department=academic_history.get("department") or "",
                    updated_at=timezone.now(),
                )
            except Exception as e:
                error_msg = f"<{__name__}> DBError: {e}"
                raise DBError(error_msg) from e

    def update_candidate_certifications(self) -> None:
        """
        候補者の資格情報を登録する
        """
        print("update_candidate_certification")
        # 既存の資格情報を削除
        old_certifications = CandidateCertification.objects.filter(
            candidate_id=self.candidate_id
        )
        for certification in old_certifications:
            print("delete certification")
            certification.delete()

        # 新しい資格情報を登録
        for certification in self.career_detail["certifications"]:
            try:
                CandidateCertification.objects.create(
                    candidate_id=self.candidate_id,
                    acquisition_date=certification.get("acquisition_date"),
                    certification=certification.get("certification") or "",
                    updated_at=timezone.now(),
                )
            except Exception as e:
                error_msg = f"<{__name__}> DBError: {e}"
                raise DBError(error_msg) from e

    def update_candidate_skills(self) -> None:
        """
        候補者のスキルを登録する
        """
        print("update_candidate_skills")
        # 既存のスキル情報を削除
        old_skills = CandidateSkill.objects.filter(candidate_id=self.candidate_id)
        for skill in old_skills:
            print("delete skill")
            skill.delete()

        # 新しいスキル情報を登録
        for skill in self.career_detail["skills"]:
            try:
                CandidateSkill.objects.create(
                    candidate_id=self.candidate_id,
                    skill=skill.get("skill") or "",
                    duration=skill.get("duration"),
                    detail=skill.get("detail") or "",
                    updated_at=timezone.now(),
                )
            except Exception as e:
                error_msg = f"<{__name__}> DBError: {e}"
                raise DBError(error_msg) from e


    def update_candidate_work_history(self) -> None:
        """
        候補者の職歴を登録する
        """
        print("update_candidate_work_history")
        # 既存の職歴情報を削除
        old_work_history = CandidateWorkHistory.objects.filter(
            candidate_id=self.candidate_id
        )
        for work_history in old_work_history:
            print("delete work_history")
            work_history.delete()

        for work_history in self.career_detail["work_history"]:
            try:
                CandidateWorkHistory.objects.create(
                    candidate_id=self.candidate_id,
                    start_date=work_history.get("start_date"),
                    end_date=work_history.get("end_date"),
                    experience=work_history.get("experience") or "",
                    detail=work_history.get("detail") or "",
                    updated_at=timezone.now(),
                )
            except Exception as e:
                error_msg = f"<{__name__}> DBError: {e}"
                raise DBError(error_msg) from e
