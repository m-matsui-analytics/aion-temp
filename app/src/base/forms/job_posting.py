import json
import os
from typing import ClassVar

import boto3
from django import forms

from base.models import (
    HTMLContentAnalysisProcess,
    JobPosting,
    JobPostingAnalysisLog,
)


class JobPostingTextCreateForm(forms.ModelForm):
    """求人票作成フォーム（テキスト）"""  # noqa: RUF002

    user = None
    text = forms.CharField(widget=forms.Textarea, required=False)
    # text = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        """メタクラス"""

        model = JobPosting
        fields: ClassVar = [
            'title',
            'url',
            'media',
            'text',
            "company",
        ]

    def save(self, commit: bool=False) -> JobPosting:
        """求人票作成処理"""
        # `text` フィールドは DB に保存されないため、フォームから削除して保存
        job_posting = super().save(commit=commit)

        # `text` フィールドの値を取得
        text = self.cleaned_data.get('text')
        if not text:
            # raise ValueError("text is required")  # エラー時に例外を発生
            job_posting.save()
            jp_log = JobPostingAnalysisLog.objects.get(job_posting=job_posting)

            start_process = HTMLContentAnalysisProcess.SELECT_IDEAL_CANDIDATE

        else:

            # `job_posting` を一度データベースに保存
            job_posting.save()

            # 開始プロセスの設定
            start_process = HTMLContentAnalysisProcess.SELECT_IDEAL_CANDIDATE

            # 解析ログにレコードを追加
            jp_log = JobPostingAnalysisLog.objects.create(
                job_posting=job_posting,
                user=self.user,
                start_process=start_process,
            )

            # s3にテキストを送信
            boto3.client("s3").put_object(
                Bucket=os.environ["AWS_S3_BUCKET_NAME"],
                Key=f"job-posting/{jp_log.id}.txt",
                Body=text,
            )
        # SQSにテキストを送信
        message_body = json.dumps(
            {
                "company_id": job_posting.company.id,
                "target_type": int(os.getenv("TARGET_TYPE_JOB_POSTING")),
                "start_process": start_process,
                "content_id": job_posting.id,
                "content_analysis_log_id": jp_log.id,
                "content_title": job_posting.title,
            },
            ensure_ascii=False
        )
        boto3.client("sqs").send_message(
            QueueUrl=os.environ["CONTENT_ANALYSIS_QUEUE_URL"],
            MessageBody=message_body,
            MessageGroupId=str(jp_log.id)
        )

        print(f"message_body: {message_body}")

        return job_posting
