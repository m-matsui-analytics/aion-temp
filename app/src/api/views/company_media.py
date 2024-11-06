from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status, views
from rest_framework.request import Request
from rest_framework.response import Response

from api.serializers import CompanyMediaDeleteSerializer, CompanyMediaSerializer
from api.views.mixins import (
    with_error_responses,
    # with_get_error_responses,
    # with_put_error_responses,
)
from api.views.responses import TypeErrorResponse
from base.models import CompanyMedia


class CompanyMediaView(views.APIView):
    """
    利用媒体ビュー
    """

    @with_error_responses('get')
    @extend_schema(
        request=CompanyMediaSerializer,
    )
    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:  # noqa: ARG002
        """取得"""
        company_id = request.user.company.id
        company_media_queryset = CompanyMedia.objects.filter(company=company_id)

        media_list = list(company_media_queryset.values_list('media', flat=True))
        return Response(media_list, status=status.HTTP_200_OK)

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
        serializer = CompanyMediaSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        company_media_queryset = CompanyMedia.objects.filter(company=company.id)
        new_media_list = list(company_media_queryset.values_list('media', flat=True))

        data = {
            "media": new_media_list
        }
        return Response(data, status=status.HTTP_201_CREATED)

    def delete(self, request: Request, *args: tuple, **kwargs: dict) -> Response:  # noqa: ARG002
        """削除"""
        company = request.user.company
        media_list = request.data.get('media')
        company_media_queryset = CompanyMedia.objects.filter(
            company=company.id,
            media__in=media_list
        )

        serializer = CompanyMediaDeleteSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        # if company_media_queryset.exists():
        company_media_queryset.delete()

        company_media_queryset = CompanyMedia.objects.filter(company=company.id)
        new_media_list = list(company_media_queryset.values_list('media', flat=True))

        data = {
            "media": new_media_list
        }
        return Response(data, status=status.HTTP_200_OK)
