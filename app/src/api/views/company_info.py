from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import views
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response

from api.serializers.company_info import CompanyInfoSerializer
from api.views.mixins import (
    with_error_responses,
    # with_get_error_responses,
    # with_put_error_responses,
)
from base.models import CompanyInfo


class CompanyInfoView(views.APIView):
    """
    会社概要のビュー
    """

    @with_error_responses('get')
    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:  # noqa: ARG002
        """取得"""
        company_id = request.user.company.id

        company_info = get_object_or_404(
            CompanyInfo,
            company=company_id,
        )

        serializer = CompanyInfoSerializer(instance=company_info)

        return Response(serializer.data)

    @with_error_responses('put')
    @extend_schema(
        # parameters=company_info_parameters
        request=CompanyInfoSerializer,
    )
    def put(self, request: Request, *args: tuple, **kwargs: dict) -> Response:  # noqa: ARG002
        """更新"""
        company_id = request.user.company.id
        company_info = get_object_or_404(
            CompanyInfo,
            company=company_id,
        )

        serializer = CompanyInfoSerializer(
            instance=company_info,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=200)

