import json
import os

import boto3
from celery import Task
from django.http import JsonResponse
from dotenv import load_dotenv

from tasks.exceptions import TaskError
from tasks.jobs.candidate_profile_updater import CandidateProfileUpdater
from tasks.jobs.career_detail_updater import CareerDetailUpdater
from tasks.jobs.gen_mail_option_updater import GenMailOptionUpdater
from tasks.jobs.ideal_candidate_match_updater import IdealCandidateMatchUpdater
from tasks.jobs.strengths_updater import StrengthsUpdater
from tasks.logger import TaskLogger

load_dotenv()

AWS_REGION = os.getenv('AWS_REGION', 'ap-northeast-1')
RECIEVE_QUEUE_URL = os.getenv("GENERATE_MAIL_RESULT_QUEUE_URL")

JOB_TYPE_CANDIDATE_PROFILE = int(os.getenv("JOB_TYPE_CANDIDATE_PROFILE"))
JOB_TYPE_CAREER_DETAIL = int(os.getenv("JOB_TYPE_CAREER_DETAIL"))
JOB_TYPE_IDEAL_CANDIDATE_MATCH = int(os.getenv("JOB_TYPE_IDEAL_CANDIDATE_MATCH"))
JOB_TYPE_GEN_MAIL_OPTION = int(os.getenv("JOB_TYPE_GEN_MAIL_OPTION"))
JOB_TYPE_APPEAL_POINT = int(os.getenv("JOB_TYPE_APPEAL_POINT"))
JOB_TYPE_LINK_CONTENTS = int(os.getenv("JOB_TYPE_LINK_CONTENTS"))
JOB_TYPE_MAIL = int(os.getenv("JOB_TYPE_MAIL"))
JOB_TYPE_MAIL_GEN_LOG = int(os.getenv("JOB_TYPE_MAIL_GEN_LOG"))

job_type_list = [
    JOB_TYPE_CANDIDATE_PROFILE,
    JOB_TYPE_CAREER_DETAIL,
    JOB_TYPE_IDEAL_CANDIDATE_MATCH,
    JOB_TYPE_GEN_MAIL_OPTION,
    JOB_TYPE_APPEAL_POINT,
    JOB_TYPE_LINK_CONTENTS,
    JOB_TYPE_MAIL,
    JOB_TYPE_MAIL_GEN_LOG
]


class MailGenDataRegisterer(Task):
    """
    メール生成システムから送信されたデータを登録するタスク
    """

    name = "mail_gen_data_registerer"

    mail_gen_log_id = None
    job_type = None

    def run(self):
        try:
            # SQSクライアントの作成
            sqs = boto3.client('sqs', region_name=AWS_REGION)  # 適切なリージョンを指定
            print("task started")
            # キューのURLを直接指定
            # queue_url = 'https://sqs.ap-northeast-1.amazonaws.com/024848476285/local_mail_gen.fifo'  # settings.pyで指定したURL

            # メッセージを受信
            response = sqs.receive_message(
                QueueUrl=RECIEVE_QUEUE_URL,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=0
            )

            messages = response.get('Messages', [])

            for message in messages:
                try:
                    print("Received message: ", message['Body'])

                    message_body = json.loads(message['Body'])

                    TaskLogger.execute(
                        message_body=message_body,
                    )

                    # 共通プロパティがない場合はエラーを出力して処理をスキップ
                    if not message_body:
                        self.error_log_handler(error_message="no message body")
                        continue

                    if not message_body.get("mail_gen_log_id"):
                        self.error_log_handler(error_message="no mail_gen_log_id")
                        continue

                    self.mail_gen_log_id = message_body["mail_gen_log_id"]

                    # JOB_TYPEがない場合は処理をスキップ
                    if not message_body.get("job_type"):
                        self.error_log_handler(error_message="no job_type")
                        continue

                    # JOB_TYPEが不正な場合はエラーを出力して処理をスキップ
                    if message_body["job_type"] not in job_type_list:
                        self.error_log_handler(error_message="invalid job_type")
                        continue

                    # JOB_TYPEによって処理を分岐
                    self.job_type=message_body["job_type"]

                    ##########################################################
                    # JOB_TYPEごとの処理
                    ##########################################################
                    # // JOB_TYPE_CANDIDATE_PROFILE //
                    if self.job_type == JOB_TYPE_CANDIDATE_PROFILE:
                        if not self.candidate_profile_validator(message_body):
                            continue
                        print("JOB_TYPE_CANDIDATE_PROFILE")

                        cp_updater = CandidateProfileUpdater(
                            candidate_id=message_body["candidate_id"],
                            candidate_profile=message_body["candidate_profile"]
                        )
                        cp_updater.update()

                    # // JOB_TYPE_CAREER_DETAIL //
                    elif self.job_type == JOB_TYPE_CAREER_DETAIL:
                        if not self.career_detail_validator(message_body):
                            continue

                        print("JOB_TYPE_CAREER_DETAIL")
                        cd_updater = CareerDetailUpdater(
                            candidate_id=message_body["candidate_id"],
                            career_detail=message_body["career_detail"]
                        )
                        cd_updater.update()

                    elif self.job_type == JOB_TYPE_IDEAL_CANDIDATE_MATCH:
                        print("JOB_TYPE_IDEAL_CANDIDATE_MATCH")
                        icm_updater = IdealCandidateMatchUpdater(
                            mail_gen_log_id=self.mail_gen_log_id,
                            candidate_id=message_body["candidate_id"],
                        )
                        icm_updater.validate(message_body)
                        icm_updater.set_ideal_candidate()
                        icm_updater.update()

                    elif self.job_type == JOB_TYPE_GEN_MAIL_OPTION:
                        print("JOB_TYPE_GEN_MAIL_OPTION")
                        gen_mail_option_updater = GenMailOptionUpdater(
                            mail_gen_log_id=self.mail_gen_log_id,
                            message_body=message_body
                        )
                        gen_mail_option_updater.set_scout_mail_id()
                        gen_mail_option_updater.set_empathy_emotion()
                        gen_mail_option_updater.set_mail_structure()
                        gen_mail_option_updater.update()

                    elif self.job_type == JOB_TYPE_APPEAL_POINT:
                        print("JOB_TYPE_APPEAL_POINT")
                        strengths_updater = StrengthsUpdater(
                            mail_gen_log_id=self.mail_gen_log_id,
                            message_body=message_body
                        )
                        strengths_updater.set_scout_mail_id()
                        strengths_updater.set_company_id()
                        strengths_updater.set_strengths()
                        strengths_updater.validate_strengths()
                        strengths_updater.update()

                    elif self.job_type == JOB_TYPE_LINK_CONTENTS:
                        print("JOB_TYPE_LINK_CONTENTS")

                    elif self.job_type == JOB_TYPE_MAIL:
                        print("JOB_TYPE_MAIL")

                    elif self.job_type == JOB_TYPE_MAIL_GEN_LOG:
                        print("JOB_TYPE_MAIL_GEN_LOG")

                    # メッセージの処理が終わったら削除
                    sqs.delete_message(
                        QueueUrl=RECIEVE_QUEUE_URL,
                        ReceiptHandle=message['ReceiptHandle']
                    )

                except ValueError as e:
                    error_message = f"ValueError: {e}"
                    self.error_log_handler(error_message)
                    continue

                except TypeError as e:
                    error_message = f"TypeError: {e}"
                    self.error_log_handler(error_message)
                    continue
                except TaskError as e:
                    print(e)
                    print("TaskError")
                    continue
        except Exception as e:
            error_message = e
            self.error_log_handler(
                error_message
            )
            return JsonResponse({"message": "error"}, status=500)

    def candidate_profile_validator(self, message_body: dict) -> bool:
        """
        候補者プロフィール用のバリデータ
        """
        print("candidate_profile_validator")
        if not message_body.get("candidate_id"):
            self.error_log_handler(error_message="no candidate_id")
            return False
        if not message_body.get("candidate_profile"):
            self.error_log_handler(error_message="no candidate_profile")
            return False

        return True

    def career_detail_validator(self, message_body: dict) -> bool:
        """
        キャリア詳細用のバリデータ
        """
        print("career_detail_validator")
        if not message_body.get("candidate_id"):
            self.error_log_handler(error_message="no candidate_id")
            return False
        if not message_body.get("career_detail"):
            self.error_log_handler(error_message="no career_detail")
            return False

        return True

    # def get_logging_config() -> dict:
    def error_log_handler(self, error_message: str) -> None:
        """
        エラーログを出力
        """
        print(error_message)
        TaskLogger.error(
            error_message=error_message,
            mail_gen_log_id=self.mail_gen_log_id,
            job_type=self.job_type
        )
# add = app.tasks[MailGenDataRegisterer.name]
# app.register_task(MailGenDataRegisterer())
