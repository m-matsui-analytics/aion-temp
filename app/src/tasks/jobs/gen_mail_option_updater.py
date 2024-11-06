import os

# from base.models.scout import Scout
from base.models.scout_mail import ScoutMail
from tasks.logger import TaskLogger

job_type = os.getenv("JOB_TYPE_GEN_MAIL_OPTION")

class GenMailOptionUpdater:
    def __init__(
            self,
            mail_gen_log_id: int,
            message_body: dict,
        ):
        self.mail_gen_log_id = mail_gen_log_id
        self.message_body = message_body
        self.scout_mail_id = None
        self.empathy_emotion = None
        self.mail_structure = None

    def set_scout_mail_id(self):
        """
        Scout Mail IDの設定
        """
        print("Set scout_mail_id")
        scout_mail = ScoutMail.objects.get(mailgenlog__id=self.mail_gen_log_id)
        # scout_mail = ScoutMail.objects.get(mail_gen_log__id=self.mail_gen_log_id)
        if not scout_mail:
            error_message = "MailGenLog not found"
            raise ValueError("MailGenLog not found")
        self.scout_mail_id = scout_mail.id
        print ("scout_mail_id: " + str(self.scout_mail_id))

    def set_empathy_emotion(self) -> None:
        """
        メールオプションの取得
        """
        print("Set empathy_emotion")
        if not self.message_body.get("empathy_emotion"):
            raise ValueError("empathy_emotion not found")

        if not isinstance(self.message_body.get("empathy_emotion"), int):
            raise TypeError("empathy_emotion is not int")

        self.empathy_emotion = self.message_body.get("empathy_emotion")
        print("empathy_emotion: " + str(self.empathy_emotion))

    def set_mail_structure(self) -> None:
        """
        メール構造の取得
        """
        if not self.message_body.get("mail_structure"):
            raise ValueError("mail_structure not found")
        if not isinstance(self.message_body.get("mail_structure"), int):
            raise TypeError("mail_structure is not int")

        self.mail_structure = self.message_body.get("mail_structure")


    def update(self) -> None:
        """
        メールオプションの更新
        """
        scout_mail = ScoutMail.objects.get(id=self.scout_mail_id)
        scout_mail.empathy_emotion=self.empathy_emotion
        scout_mail.mail_structure=self.mail_structure
        scout_mail.save()

    def log_error(self, error_message: str) -> None:
        """
        エラーログの出力
        """
        TaskLogger.error(
            error_message=error_message,
            log_id=self.mail_gen_log_id,
            job_type=job_type
        )
