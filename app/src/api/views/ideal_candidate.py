from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status, views
from rest_framework.request import Request
from rest_framework.response import Response

from api.serializers import IdealCandidateSerializer
from api.views.mixins import (
    with_error_responses,
    # with_get_error_responses,
    # with_put_error_responses,
)
from api.views.responses import TypeErrorResponse
from base.models import IdealCandidate


class IdealCandidateListView(views.APIView):
    """
    利用媒体一覧ビュー
    """

    @with_error_responses('get')
    @extend_schema(
        request=IdealCandidateSerializer(many=True),
    )
    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:  # noqa: ARG002
        """取得"""
        company_id = request.user.company.id
        ideal_candidate = IdealCandidate.objects.filter(company=company_id)
        serializer = IdealCandidateSerializer(instance=ideal_candidate, many=True)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class IdealCandidateView(views.APIView):
    """
    利用媒体一覧ビュー
    """

    @with_error_responses('get')
    @extend_schema(
        request=IdealCandidateSerializer(many=True),
    )
    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:  # noqa: ARG002
        """取得"""
        company_id = request.user.company.id
        ideal_candidate_id = kwargs.get('id')

        if ideal_candidate_id is None:
            return Response({"error": "ideal_candidate_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        # 該当するIdealCandidateオブジェクトを取得
        ideal_candidate = get_object_or_404(IdealCandidate, id=ideal_candidate_id)

        ideal_candidate = IdealCandidate.objects.filter(
            company=company_id,
            ideal_candidate=ideal_candidate_id
        )
        serializer = IdealCandidateSerializer(instance=ideal_candidate, many=True)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @with_error_responses('post')
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name=None,
                type=OpenApiTypes.ANY,
                location=OpenApiParameter.QUERY,
                required=True,
                description="媒体IDリスト"
            )
        ],
        # parameters=company_media_parameters
        request=[],
    )
    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:  # noqa: ARG002
        """更新"""
        company = request.user.company
        media_list = request.data.get('media')

        if not isinstance(media_list, list):
            return TypeErrorResponse("media_list")

        # 会社概要の更新
        serializer = IdealCandidateSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        company_media_queryset = IdealCandidate.objects.filter(company=company.id)
        new_media_list = list(company_media_queryset.values_list('media', flat=True))

        data = {
            "media": new_media_list
        }
        return Response(data, status=status.HTTP_201_CREATED)

    # def delete(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
    #     """削除"""
    #     company = request.user.company
    #     media_list = request.data.get('media')
    #     company_media_queryset = IdealCandidate.objects.filter(
    #         company=company.id,
    #         media__in=media_list
    #     )

    #     serializer = IdealCandidateSerializer(
    #         data=request.data,
    #         context={'request': request}
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     # if company_media_queryset.exists():
    #     company_media_queryset.delete()

    #     company_media_queryset = IdealCandidate.objects.filter(company=company.id)
    #     new_media_list = list(company_media_queryset.values_list('media', flat=True))

    #     data = {
    #         "media": new_media_list
    #     }
    #     return Response(data, status=status.HTTP_200_OK)
