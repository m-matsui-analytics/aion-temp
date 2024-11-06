import json
import os

import boto3
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status, views
from rest_framework.request import Request
from rest_framework.response import Response

from api.logger import APIErrorLogger
from api.serializers import (
    RecruitmentArticleCreateTextSerializer,
    RecruitmentArticleCreateURLSerializer,
    RecruitmentArticleListSerializer,
    RecruitmentArticleSerializer,
)
from api.views.mixins import (
    with_error_responses,
)
from api.views.responses import TypeErrorResponse
from base.models import RecruitmentArticle, RecruitmentArticleAnalysisLog, HTMLContentAnalysisProcess


class RecruitmentArticleView(views.APIView):
    """
    採用記事一覧ビュー
    """

    @with_error_responses("get")
    @extend_schema(responses={200: RecruitmentArticle, 401: None, 403: None})
    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:  # noqa: ARG002
        """一覧取得"""
        company_id = request.user.company.id
        ra_queryset = RecruitmentArticle.objects.filter(
            company=company_id
        )  # クエリセットを取得

        # クエリセットをシリアライズ
        serializer = RecruitmentArticleSerializer(ra_queryset, many=True)

        # シリアライズされたデータをレスポンスとして返す
        return Response(serializer.data, status=status.HTTP_200_OK)



class RecruitmentArticleCreateURLView(views.APIView):
    """
    採用記事登録（URL）ビュー
    """  # noqa: RUF002

    @with_error_responses("post")
    @extend_schema(
        request=RecruitmentArticleCreateURLSerializer,
        responses={201: RecruitmentArticleCreateURLSerializer, 400: None, 401: None, 403: None},
    )
    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:  # noqa: ARG002
        """追加"""
        data = {
            "title": request.data.get("title", ""),
            "url": request.data.get("url"),
            "media": request.data.get("media"),
        }

        # 会社概要の更新
        serializer = RecruitmentArticleCreateURLSerializer(
            data=data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({}, status=status.HTTP_201_CREATED)


class RecruitmentArticleCreateTextView(views.APIView):
    """
    採用記事登録（テキスト）ビュー
    """  # noqa: RUF002

    @with_error_responses("post")
    @extend_schema(
        request=RecruitmentArticleCreateTextSerializer,
        responses={
            201: RecruitmentArticleCreateTextSerializer,
            400: None,
            401: None,
            403: None,
        },
    )
    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:  # noqa: ARG002
        """追加"""
        try:
            data = {
                "url": request.data.get("url"),
                "title": request.data.get("title"),
                "media": request.data.get("media"),
            }

            # 会社概要の更新
            serializer = RecruitmentArticleCreateTextSerializer(
                data=data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            recruitment_article = serializer.save()

            text = request.data.get("text")
            if not text:
                error_message = "text is required"
                APIErrorLogger.error(error_message)
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


            start_process = HTMLContentAnalysisProcess.SELECT_IDEAL_CANDIDATE

            # 解析ログにレコードを追加
            ra_log = RecruitmentArticleAnalysisLog.objects.create(
                recruitment_article=recruitment_article,
                user=request.user,
                start_process=start_process,
            )

            # s3にテキストを送信
            boto3.client("s3").put_object(
                Bucket=os.environ["AWS_S3_BUCKET_NAME"],
                Key=f"recruitment-article/{ra_log.id}.txt",
                Body=text,
            )
            print(start_process)
            # SQSにテキストを送信
            message_body = json.dumps(
                {
                    "company_id": request.user.company.id,
                    "target_type": os.getenv("TARGET_TYPE_RECRUITMENT_ARTICLE"),
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
            return Response({}, status=status.HTTP_201_CREATED)
        except Exception as e:
            APIErrorLogger.error(e)
            raise e
