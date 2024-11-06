import os

from base.models.ideal_candidate import IdealCandidate
from base.models.scout import Scout
from tasks.logger import TaskLogger

job_type = os.getenv("JOB_TYPE_IDEAL_CANDIDATE_MATCH")

class IdealCandidateMatchUpdater:
    def __init__(
            self,
            mail_gen_log_id: int,
            candidate_id: int,
        ):
        self.mail_gen_log_id = mail_gen_log_id
        self.candidate_id = candidate_id
        self.ideal_candidate_id = None
        self.ideal_candidate = None
        self.matching_rate  = None
        self.is_matched = None
        self.reason = ""

    def update(self):

        Scout.objects.filter(candidate_id=self.candidate_id).update(
            ideal_candidate=self.ideal_candidate,
            matching_rate=self.matching_rate,
            is_matched=self.is_matched,
            reason=self.reason
        )

    def validate(self, message_body: dict) -> dict:
        """
        メッセージのバリデーション
        """
        self.validate_ideal_candidate_id(message_body)
        self.validate_matching_rate(message_body)
        self.validate_is_matched(message_body)
        self.validate_reason(message_body)


    def validate_ideal_candidate_id(self, message_body: dict) -> None:
        """
        ideal_candidate_idのバリデーション
        """
        ideal_candidate_id = message_body.get("ideal_candidate_id")
        print("ideal_candidate_id"+ str(ideal_candidate_id))

        if ideal_candidate_id is None:
            self.log_error("no ideal_candidate_id")
            self.ideal_candidate_id = None
            return

        if not isinstance(ideal_candidate_id, int):
            self.log_error("ideal_candidate_id is not int")
            self.ideal_candidate_id = None
            return

        if not IdealCandidate.objects.filter(id=ideal_candidate_id).exists():
            self.log_error("ideal_candidate_id is not found")
            self.ideal_candidate_id = None
            return

        self.ideal_candidate_id = ideal_candidate_id


    def validate_matching_rate(self, message_body: dict) -> None:
        """
        matching_rateのバリデーション
        """
        if not message_body.get("matching_rate"):
            self.log_error("no matching_rate")
            self.matching_rate = None

        elif not isinstance(message_body["matching_rate"], float):
            self.log_error("matching_rate is not float")
            self.matching_rate = None

        self.matching_rate = message_body.get("matching_rate")

    def validate_is_matched(self, message_body: dict) -> None:
        """
        is_matchedのバリデーション
        """
        if not message_body.get("is_matched"):
            self.log_error("no is_matched")
        elif not isinstance(message_body["is_matched"], bool):
            self.log_error("is_matched is not bool")

        self.is_matched = message_body.get("is_matched")

    def validate_reason(self, message_body: dict) -> None:
        """
        reasonのバリデーション
        """
        if not message_body.get("reason"):
            self.log_error("no reason")
        elif not isinstance(message_body["reason"], str):
            self.log_error("reason is not str")

        self.reason = message_body.get("reason")

    def set_ideal_candidate(self) -> None:
        """
        ideal_candidateをセットする
        """
        self.ideal_candidate = IdealCandidate.objects.get(id=self.ideal_candidate_id)

    def log_error(self, error_message: str) -> None:
        """
        エラーログを出力する
        """
        print(error_message)
        TaskLogger.error(
            error_message=error_message,
            mail_gen_log_id=self.mail_gen_log_id,
            job_type=job_type
        )

