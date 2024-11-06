
import json
import os

import boto3
from celery import Task
from django.http import JsonResponse
from dotenv import load_dotenv

from tasks.exceptions import TaskError
from tasks.jobs.content_analysis_updater import ContentAnalysisUpdater
# from tasks.jobs.candidate_profile_updater import CandidateProfileUpdater
# from tasks.jobs.career_detail_updater import CareerDetailUpdater
# from tasks.jobs.gen_mail_option_updater import GenMailOptionUpdater
# from tasks.jobs.ideal_candidate_match_updater import IdealCandidateMatchUpdater
# from tasks.jobs.strengths_updater import StrengthsUpdater
from tasks.logger import TaskLogger

load_dotenv()

AWS_REGION = os.getenv('AWS_REGION', 'ap-northeast-1')
RECIEVE_QUEUE_URL = os.getenv("CONTENT_ANALYSIS_RESULT_QUEUE_URL")

JOB_TYPE_ANALYSIS_RESULT = os.getenv("JOB_TYPE_ANALYSIS_RESULT")
job_type_list = [
    JOB_TYPE_ANALYSIS_RESULT,
]


TARGET_TYPE_JOB_POSTING = int(os.getenv("TARGET_TYPE_JOB_POSTING"))
TARGET_TYPE_RECRUITMENT_ARTICLE = int(os.getenv("TARGET_TYPE_RECRUITMENT_ARTICLE"))
target_type_list = [
    TARGET_TYPE_JOB_POSTING,
    TARGET_TYPE_RECRUITMENT_ARTICLE,
]

class ContentAnalysisResultRegisterer(Task):
    """
    コンテンツ解析システムから送信されたデータを登録するタスク
    """

    name = "content_analysis_result_registerer"

    content_analysis_log_id = None
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

                    if not message_body.get("content_analysis_log_id"):
                        self.error_log_handler(error_message="no content_analysis_log_id")
                        continue

                    self.content_analysis_log_id = message_body["content_analysis_log_id"]

                    # target_typeがない場合は処理をスキップ
                    if not message_body.get("target_type"):
                        self.error_log_handler(error_message="no target_type")
                        continue

                    # target_typeが不正な場合はエラーを出力して処理をスキップ
                    if message_body["target_type"] not in target_type_list:
                        self.error_log_handler(error_message="invalid target_type")
                        continue
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
                    # // JOB_TYPE_ANALYSIS_RESULT //
                    if self.job_type == JOB_TYPE_ANALYSIS_RESULT:
                        print("JOB_TYPE_ANALYSIS_RESULT")
                        ca_updater = ContentAnalysisUpdater(
                            company_id=message_body["company_id"],
                            target_type=message_body["target_type"],
                            content_id=message_body["content_id"],
                            content_analysis_log_id=self.content_analysis_log_id,
                            result=message_body["result"]
                        )
                        ca_updater.validate()
                        ca_updater.update()
    #                 # // JOB_TYPE_CANDIDATE_PROFILE //
    #                 if self.job_type == JOB_TYPE_CANDIDATE_PROFILE:
    #                     if not self.candidate_profile_validator(message_body):
    #                         continue
    #                     print("JOB_TYPE_CANDIDATE_PROFILE")

    #                     cp_updater = CandidateProfileUpdater(
    #                         candidate_id=message_body["candidate_id"],
    #                         candidate_profile=message_body["candidate_profile"]
    #                     )
    #                     cp_updater.update()

    #                 # // JOB_TYPE_CAREER_DETAIL //
    #                 elif self.job_type == JOB_TYPE_CAREER_DETAIL:
    #                     if not self.career_detail_validator(message_body):
    #                         continue

    #                     print("JOB_TYPE_CAREER_DETAIL")
    #                     cd_updater = CareerDetailUpdater(
    #                         candidate_id=message_body["candidate_id"],
    #                         career_detail=message_body["career_detail"]
    #                     )
    #                     cd_updater.update()

    #                 elif self.job_type == JOB_TYPE_IDEAL_CANDIDATE_MATCH:
    #                     print("JOB_TYPE_IDEAL_CANDIDATE_MATCH")
    #                     icm_updater = IdealCandidateMatchUpdater(
    #                         content_analysis_log_id=self.content_analysis_log_id,
    #                         candidate_id=message_body["candidate_id"],
    #                     )
    #                     icm_updater.validate(message_body)
    #                     icm_updater.set_ideal_candidate()
    #                     icm_updater.update()

    #                 elif self.job_type == JOB_TYPE_GEN_MAIL_OPTION:
    #                     print("JOB_TYPE_GEN_MAIL_OPTION")
    #                     gen_mail_option_updater = GenMailOptionUpdater(
    #                         content_analysis_log_id=self.content_analysis_log_id,
    #                         message_body=message_body
    #                     )
    #                     gen_mail_option_updater.set_scout_mail_id()
    #                     gen_mail_option_updater.set_empathy_emotion()
    #                     gen_mail_option_updater.set_mail_structure()
    #                     gen_mail_option_updater.update()

    #                 elif self.job_type == JOB_TYPE_APPEAL_POINT:
    #                     print("JOB_TYPE_APPEAL_POINT")
    #                     strengths_updater = StrengthsUpdater(
    #                         content_analysis_log_id=self.content_analysis_log_id,
    #                         message_body=message_body
    #                     )
    #                     strengths_updater.set_scout_mail_id()
    #                     strengths_updater.set_company_id()
    #                     strengths_updater.set_strengths()
    #                     strengths_updater.validate_strengths()
    #                     strengths_updater.update()

    #                 elif self.job_type == JOB_TYPE_LINK_RECRUITMENT_ARTICLE:
    #                     print("JOB_TYPE_LINK_RECRUITMENT_ARTICLE")

    #                 elif self.job_type == JOB_TYPE_MAIL:
    #                     print("JOB_TYPE_MAIL")

    #                 elif self.job_type == JOB_TYPE_MAIL_GEN_LOG:
    #                     print("JOB_TYPE_MAIL_GEN_LOG")

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
            # # メッセージの処理が終わったら削除
            # sqs.delete_message(
            #     QueueUrl=RECIEVE_QUEUE_URL,
            #     ReceiptHandle=message['ReceiptHandle']
            # )
            return JsonResponse({"message": "error"}, status=500)

    # def candidate_profile_validator(self, message_body: dict) -> bool:
    #     """
    #     候補者プロフィール用のバリデータ
    #     """
    #     print("candidate_profile_validator")
    #     if not message_body.get("candidate_id"):
    #         self.error_log_handler(error_message="no candidate_id")
    #         return False
    #     if not message_body.get("candidate_profile"):
    #         self.error_log_handler(error_message="no candidate_profile")
    #         return False

    #     return True

    # def career_detail_validator(self, message_body: dict) -> bool:
    #     """
    #     キャリア詳細用のバリデータ
    #     """
    #     print("career_detail_validator")
    #     if not message_body.get("candidate_id"):
    #         self.error_log_handler(error_message="no candidate_id")
    #         return False
    #     if not message_body.get("career_detail"):
    #         self.error_log_handler(error_message="no career_detail")
    #         return False

    #     return True

    # def get_logging_config() -> dict:
    def error_log_handler(self, error_message: str) -> None:
        """
        エラーログを出力
        """
        print(error_message)
        TaskLogger.error(
            error_message=error_message,
            log_id=self.content_analysis_log_id,
            job_type=self.job_type
        )
# add = app.tasks[MailGenDataRegisterer.name]
# app.register_task(MailGenDataRegisterer())
