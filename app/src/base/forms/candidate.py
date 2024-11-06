import json
import os
from typing import ClassVar

import boto3
from django import forms

from base.models import (
    Candidate,
    MailGenLog,
    MailGenProcess,
    Scout,
    ScoutMail,
)

class CandidateCreateForm(forms.ModelForm):
    """候補者作成フォーム"""

    text = forms.CharField(widget=forms.Textarea, required=False)
    # text = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        """メタクラス"""

        model = Candidate
        fields: ClassVar = [
            "company",
            "media",
            "id_in_media",
            "text",
        ]

    def save(self, commit: bool=False) -> Candidate:
        """候補者作成処理"""
        # `text` フィールドは DB に保存されないため、フォームから削除して保存
        candidate = super().save(commit=commit)

        # `text` フィールドの値を取得
        text = self.cleaned_data.get('text')
        if not text:
            # raise ValueError("text is required")  # エラー時に例外を発生
            candidate.save()
            scout = Scout.objects.create(candidate=candidate)
            scout_mail = ScoutMail.objects.create(scout=scout)
            mail_gen_log = MailGenLog.objects.create(
                scout=scout,
                scout_mail=scout_mail,
                start_process = MailGenProcess.EXTRACT_CANDIDATE_PROFILE
            )

        else:

            # `job_posting` を一度データベースに保存
            candidate.save()

            # 開始プロセスの設定
            start_process = MailGenProcess.EXTRACT_CANDIDATE_PROFILE
            scout = Scout.objects.create(candidate=candidate)
            scout_mail = ScoutMail.objects.create(scout=scout)
            mail_gen_log = MailGenLog.objects.create(
                scout=scout,
                scout_mail=scout_mail,
                user=self.user,
                start_process=start_process,
            )
            # # メール作成
            # mail_gen_log = MailGenLog.objects.create(
            #     candidate=candidate,
            #     user=self.user,
            #     start_process=start_process,
            # )

            # s3 に保存
            boto3.client('s3').put_object(
                Bucket=os.getenv('AWS_S3_BUCKET_NAME'),
                Key=f'candidate-raw-data/{mail_gen_log.id}.txt',
                Body=text,
            )

        message_body = json.dumps(
            {
                'mail_gen_log_id': mail_gen_log.id,
                'start_process': start_process,
                "candidate_id": candidate.id,
                "company_id": candidate.company.id,
            },
            ensure_ascii=False
        )
        boto3.client('sqs').send_message(
            QueueUrl=os.getenv('GENERATE_MAIL_QUEUE_URL'),
            MessageBody=message_body,
            MessageGroupId=str(mail_gen_log.id)
        )

        return candidate
