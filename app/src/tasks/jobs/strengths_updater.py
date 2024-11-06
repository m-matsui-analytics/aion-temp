import os

from base.models.company_strength import CompanyStrength
from base.models.mail_gen_log import MailGenLog
from base.models.scout_mail import ScoutMail

job_type = os.getenv("JOB_TYPE_APPEAL_POINT")

class StrengthsUpdater:
    def __init__(
            self,
            mail_gen_log_id: int,
            message_body: dict,
        ):
        self.mail_gen_log_id = mail_gen_log_id
        self.message_body = message_body
        self.scout_mail_id = None
        self.strengths = None
        self.company_id = None

    def set_scout_mail_id(self):
        """
        Scout Mail IDの設定
        """
        print("Set scout_mail_id")
        scout_mail = ScoutMail.objects.get(mailgenlog__id=self.mail_gen_log_id)
        if not scout_mail:
            raise ValueError("MailGenLog not found")
        self.scout_mail_id = scout_mail.id
        print ("scout_mail_id: " + str(self.scout_mail_id))

    def set_company_id(self):
        """
        企業IDの設定
        """
        scout_mail = ScoutMail.objects.get(id=self.scout_mail_id)
        self.company_id = scout_mail.scout.candidate.company_id
        print("company_id: " + str(self.company_id))

    def set_strengths(self) -> None:
        """
        メールで利用する企業の強みの取得
        """
        if not self.message_body.get("strengths"):
            raise ValueError("strengths not found")
        if not isinstance(self.message_body.get("strengths"), list):
            raise TypeError("strengths is not str")

        self.strengths = self.message_body.get("strengths")
        print("strengths: " + str(self.strengths))

    def validate_strengths(self) -> None:
        """
        メールで利用する企業の強みのバリデーション
        """
        for strength in self.strengths:
            if not strength.get("strength_id"):
                raise ValueError("strength_id not found")
            if not isinstance(strength.get("strength_id"), int):
                raise TypeError("strength_id is not int")
            if not CompanyStrength.objects.filter(
                        id=strength["strength_id"], company_id=self.company_id
                    ).exists():
                raise ValueError("strength_id is not found")
            if strength.get("reason") and not isinstance(strength.get("reason"), str):
                raise TypeError("reason is not str")

    def update(self) -> None:
        """
        メールで利用する企業の強みの更新
        """
        scout_mail = ScoutMail.objects.get(id=self.scout_mail_id)

        scout_mail.strength_1 = CompanyStrength.objects.get(
                                    id=self.strengths[0]["strength_id"],
                                    company_id=self.company_id
                                )

        if self.strengths[1]:
            scout_mail.strength_2 = CompanyStrength.objects.get(
                id=self.strengths[1].get("strength_id")
            )
        if self.strengths[2]:
            scout_mail.strength_3 = CompanyStrength.objects.get(
                id=self.strengths[2].get("strength_id")
            )

        scout_mail.save()

