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

class DeleteMessage(Task):
    name = "delete_message"

    def run(self):


        # SQSクライアントの作成
        sqs = boto3.client('sqs')

        # キューURLの設定
        queue_url = 'https://sqs.ap-northeast-1.amazonaws.com/024848476285/local_content_analysis_result.fifo'
        # queue_url = 'https://sqs.ap-northeast-1.amazonaws.com/024848476285/local_content_analysis.fifo'

        # メッセージの再取得
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10
        )

        if 'Messages' in response:
            print(len(response['Messages']), '個のメッセージを取得しました。')
            for message in response.get('Messages', []):
                # メッセージIDと新しいリシートハンドルを取得
                    # message = response['Messages'][0]
                receipt_handle = message['ReceiptHandle']

                # メッセージの削除
                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=receipt_handle
                )
                print("メッセージが削除されました。")
        else:
            print("メッセージが見つかりません。")

