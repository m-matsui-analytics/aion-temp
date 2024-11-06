import json
import os
from typing import ClassVar

import boto3
from django import forms

from base.models import (
    HTMLContentAnalysisProcess,
    RecruitmentArticle,
    RecruitmentArticleAnalysisLog,
)


class RecruitmentArticleTextCreateForm(forms.ModelForm):
    """採用記事作成フォーム（テキスト）"""  # noqa: RUF002

    user = None
    text = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        """メタクラス"""

        model = RecruitmentArticle
        fields: ClassVar = [
            'title',
            'url',
            'media',
            'text',
            "company",
        ]

    def save(self, commit: bool=False) -> RecruitmentArticle:  # noqa: FBT001, FBT002
        """採用記事作成処理"""
        # `text` フィールドは DB に保存されないため、フォームから削除して保存
        recruitment_article = super().save(commit)

        # `text` フィールドの値を取得
        text = self.cleaned_data.get('text')
        if not text:
            recruitment_article.save()
            ra_log = RecruitmentArticleAnalysisLog.objects.get(
                recruitment_article=recruitment_article
            )
            start_process = HTMLContentAnalysisProcess.SELECT_IDEAL_CANDIDATE

            # raise ValueError("text is required")  # エラー時に例外を発生
        else:
            # `recruitment_article` を一度データベースに保存
            recruitment_article.save()

            # 開始プロセスの設定
            start_process = HTMLContentAnalysisProcess.SELECT_IDEAL_CANDIDATE

            # 解析ログにレコードを追加
            ra_log = RecruitmentArticleAnalysisLog.objects.create(
                recruitment_article=recruitment_article,
                user=self.user,
                start_process=start_process,
            )

            # s3にテキストを送信
            boto3.client("s3").put_object(
                Bucket=os.environ["AWS_S3_BUCKET_NAME"],
                Key=f"recruitment-article/{ra_log.id}.txt",
                Body=text,
            )

        # SQSにテキストを送信
        message_body = json.dumps(
            {
                "company_id": recruitment_article.company.id,
                "target_type": int(os.getenv("TARGET_TYPE_RECRUITMENT_ARTICLE")),
                "start_process": start_process,
                "content_id": recruitment_article.id,
                "content_analysis_log_id": ra_log.id,
                "content_title": recruitment_article.title,
            },
            ensure_ascii=False
        )
        boto3.client("sqs").send_message(
            QueueUrl=os.environ["CONTENT_ANALYSIS_QUEUE_URL"],
            MessageBody=message_body,
            MessageGroupId=str(ra_log.id)
        )
        print(f"message_body: {message_body}")

        return recruitment_article
