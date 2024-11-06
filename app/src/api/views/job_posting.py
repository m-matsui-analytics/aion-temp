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
    JobPostingCreateTextSerializer,
    JobPostingCreateURLSerializer,
    JobPostingListSerializer,
    JobPostingSerializer,
)
from api.views.mixins import (
    with_error_responses,
    # with_get_error_responses,
    # with_put_error_responses,
)
from api.views.responses import TypeErrorResponse
from base.models import JobPosting, JobPostingAnalysisLog, HTMLContentAnalysisProcess


class JobPostingView(views.APIView):
    """
    求人票一覧ビュー
    """

    @with_error_responses("get")
    @extend_schema(responses={200: JobPosting, 401: None, 403: None})
    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:  # noqa: ARG002
        """一覧取得"""
        company_id = request.user.company.id
        jp_queryset = JobPosting.objects.filter(
            company=company_id
        )  # クエリセットを取得

        # クエリセットをシリアライズ
        serializer = JobPostingSerializer(jp_queryset, many=True)

        # シリアライズされたデータをレスポンスとして返す
        return Response(serializer.data, status=status.HTTP_200_OK)

    # @with_error_responses('post')
    # @extend_schema(
    #     request=JobPostingSerializer,
    #     responses={
    #         200: JobPostingListSerializer,
    #         401: None,
    #         403: None
    #     }
    # )
    # def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:  # noqa: ARG002
    #     """追加"""
    #     data = {
    #         "company": request.user.company,
    #         "title": request.data.get('title', ""),
    #         "url": request.data.get('url', ""),
    #         "media": request.data.get('media'),
    #     }

    #     # 会社概要の更新
    #     serializer = JobPostingSerializer(data=data, context={'request': request})
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     return Response({}, status=status.HTTP_201_CREATED)


class JobPostingCreateURLView(views.APIView):
    """
    求人票登録（URL）ビュー
    """  # noqa: RUF002

    @with_error_responses("post")
    @extend_schema(
        request=JobPostingCreateURLSerializer,
        responses={201: JobPostingCreateURLSerializer, 400: None, 401: None, 403: None},
    )
    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:  # noqa: ARG002
        """追加"""
        data = {
            "title": request.data.get("title", ""),
            "url": request.data.get("url"),
            "media": request.data.get("media"),
        }

        # 会社概要の更新
        serializer = JobPostingCreateURLSerializer(
            data=data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({}, status=status.HTTP_201_CREATED)


class JobPostingCreateTextView(views.APIView):
    """
    求人票登録（テキスト）ビュー
    """  # noqa: RUF002

    @with_error_responses("post")
    @extend_schema(
        request=JobPostingCreateTextSerializer,
        responses={
            201: JobPostingCreateTextSerializer,
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
            serializer = JobPostingCreateTextSerializer(
                data=data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            job_posting = serializer.save()

            text = request.data.get("text")
            if not text:
                error_message = "text is required"
                APIErrorLogger.error(error_message)
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


            start_process = HTMLContentAnalysisProcess.SELECT_IDEAL_CANDIDATE

            # 解析ログにレコードを追加
            jp_log = JobPostingAnalysisLog.objects.create(
                job_posting=job_posting,
                user=request.user,
                start_process=start_process,
            )

            # s3にテキストを送信
            boto3.client("s3").put_object(
                Bucket=os.environ["AWS_S3_BUCKET_NAME"],
                Key=f"job-posting/{jp_log.id}.txt",
                Body=text,
            )
            print(start_process)
            # SQSにテキストを送信
            message_body = json.dumps(
                {
                    "company_id": request.user.company.id,
                    "target_type": os.getenv("TARGET_TYPE_JOB_POSTING"),
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
            return Response({}, status=status.HTTP_201_CREATED)
        except Exception as e:
            APIErrorLogger.error(e)
            raise e

# class JobPostingDetailView(views.APIView):
#     """
#     利用媒体詳細ビュー
#     """
#     @with_error_responses('get')
#     @extend_schema(
#         request=JobPostingSerializer,
#     )
#     def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:  # noqa: ARG002
#         """取得"""
#         company_id = request.user.company.id
#         job_posting_queryset = JobPosting.objects.filter(company=company_id)

#         media_list = list(job_posting_queryset.values_list('media', flat=True))
#         return Response(media_list, status=status.HTTP_200_OK)

#     @with_error_responses('post')
#     @extend_schema(
#         parameters=[
#             OpenApiParameter(
#                 name=None,
#                 type=OpenApiTypes.ANY,
#                 location=OpenApiParameter.QUERY,
#                 required=True,
#                 description="媒体IDリスト"
#             )
#         ],
#         # parameters=job_posting_parameters
#         request=[],
#     )
#     def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:  # noqa: ARG002
#         """更新"""
#         company = request.user.company
#         media_list = request.data.get('media')

#         if not isinstance(media_list, list):
#             return TypeErrorResponse("media_list")

#         # 会社概要の更新
#         serializer = JobPostingSerializer(
#             data=request.data,
#             context={'request': request}
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         job_posting_queryset = JobPosting.objects.filter(company=company.id)
#         new_media_list = list(job_posting_queryset.values_list('media', flat=True))

#         data = {
#             "media": new_media_list
#         }
#         return Response(data, status=status.HTTP_201_CREATED)

#     def delete(self, request: Request, *args: tuple, **kwargs: dict) -> Response:  # noqa: ARG002
#         """削除"""
#         company = request.user.company
#         media_list = request.data.get('media')
#         job_posting_queryset = JobPosting.objects.filter(
#             company=company.id,
#             media__in=media_list
#         )

#         serializer = JobPostingDeleteSerializer(
#             data=request.data,
#             context={'request': request}
#         )
#         serializer.is_valid(raise_exception=True)
#         # if job_posting_queryset.exists():
#         job_posting_queryset.delete()

#         job_posting_queryset = JobPosting.objects.filter(company=company.id)
#         new_media_list = list(job_posting_queryset.values_list('media', flat=True))

#         data = {
#             "media": new_media_list
#         }
#         return Response(data, status=status.HTTP_200_OK)
